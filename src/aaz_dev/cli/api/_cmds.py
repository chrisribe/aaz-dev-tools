import click
import logging
from flask import Blueprint
import sys
import subprocess
import os

from utils.config import Config

logger = logging.getLogger('backend')

bp = Blueprint('cli-cmds', __name__, url_prefix='/CLI/CMDs', cli_group="cli")
bp.cli.short_help = "Manage aaz commands in azure-cli and azure-cli-extensions."


@bp.cli.command("regenerate", short_help="Regenerate aaz commands from command models in azure-cli/azure-cli-extensions")
@click.option(
    "--aaz-path", '-a',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    default=Config.AAZ_PATH,
    required=not Config.AAZ_PATH,
    callback=Config.validate_and_setup_aaz_path,
    expose_value=False,
    help="The local path of aaz repo."
)
@click.option(
    "--cli-path", '-c',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    callback=Config.validate_and_setup_cli_path,
    help="The local path of azure-cli repo. Only required when generate code to azure-cli repo."
)
@click.option(
    "--cli-extension-path", '-e',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    callback=Config.validate_and_setup_cli_extension_path,
    help="The local path of azure-cli-extension repo. Only required when generate code to azure-cli-extension repo."
)
@click.option(
    "--extension-or-module-name", '--name',
    required=True,
    help="Name of the module in azure-cli or the extension in azure-cli-extensions"
)
def regenerate_code(extension_or_module_name, cli_path=None, cli_extension_path=None):
    from utils.config import Config
    from utils.exceptions import InvalidAPIUsage
    from cli.controller.az_module_manager import AzExtensionManager, AzMainManager
    if not cli_path and not cli_extension_path:
        logger.error("Please provide `--cli-path` or `--cli-extension-path`")
        sys.exit(1)
    if cli_path and cli_extension_path:
        logger.error("Please don't provide `--cli-path` and `--cli-extension-path`")
        sys.exit(1)

    try:
        if cli_path is not None:
            assert Config.CLI_PATH is not None
            manager = AzMainManager()
        else:
            assert cli_extension_path is not None
            assert Config.CLI_EXTENSION_PATH is not None
            manager = AzExtensionManager()

        if not manager.has_module(extension_or_module_name):
            # module = manager.create_new_mod(extension_or_module_name)
            raise ValueError(f"Cannot find module or extension `{extension_or_module_name}`")
        logger.info(f"Load module `{extension_or_module_name}`")
        module = manager.load_module(extension_or_module_name)
        logger.info(f"Regenerate module `{extension_or_module_name}`")
        manager.update_module(extension_or_module_name, module.profiles)
    except InvalidAPIUsage as err:
        logger.error(err)
        sys.exit(1)
    except ValueError as err:
        logger.error(err)
        sys.exit(1)


@bp.cli.command("generate-by-swagger-tag", short_help="Generate aaz commands from command models in azure-cli/azure-cli-extensions selected by swagger tags.")
@click.option(
    "--aaz-path", '-a',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    default=Config.AAZ_PATH,
    required=not Config.AAZ_PATH,
    callback=Config.validate_and_setup_aaz_path,
    expose_value=False,
    help="The local path of aaz repo."
)
@click.option(
    "--cli-path", '-c',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    callback=Config.validate_and_setup_cli_path,
    help="The local path of azure-cli repo. Only required when generate code to azure-cli repo."
)
@click.option(
    "--cli-extension-path", '-e',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    callback=Config.validate_and_setup_cli_extension_path,
    help="The local path of azure-cli-extension repo. Only required when generate code to azure-cli-extension repo."
)
@click.option(
    "--extension-or-module-name", '--name',
    required=True,
    help="Name of the module in azure-cli or the extension in azure-cli-extensions"
)
@click.option(
    "--swagger-module-path", "--sm",
    type=click.Path(file_okay=False, dir_okay=True, readable=True, resolve_path=True),
    default=Config.SWAGGER_MODULE_PATH,
    required=not Config.SWAGGER_MODULE_PATH,
    callback=Config.validate_and_setup_swagger_module_path,
    expose_value=False,
    help="The local path of swagger module."
)
@click.option(
    "--resource-provider", "--rp",
    default=Config.DEFAULT_RESOURCE_PROVIDER,
    required=not Config.DEFAULT_RESOURCE_PROVIDER,
    callback=Config.validate_and_setup_default_resource_provider,
    expose_value=False,
    help="The resource provider name."
)
@click.option(
    "--swagger-tag", "--tag",
    required=True,
    help="Swagger tag with input files."
)
@click.option(
    "--profile",
    required=True,
    type=click.Choice(Config.CLI_PROFILES),
    default=Config.CLI_DEFAULT_PROFILE,
)
def generate_by_swagger_tag(profile, swagger_tag, extension_or_module_name, cli_path=None, cli_extension_path=None):
    from utils.config import Config
    from utils.exceptions import InvalidAPIUsage
    from cli.controller.az_module_manager import AzExtensionManager, AzMainManager
    from swagger.controller.specs_manager import SwaggerSpecsManager
    from command.controller.specs_manager import AAZSpecsManager
    if not Config.DEFAULT_SWAGGER_MODULE:
        Config.DEFAULT_SWAGGER_MODULE = "__MODULE__"

    try:
        swagger_specs = SwaggerSpecsManager()
        aaz_specs = AAZSpecsManager()
        module_manager = swagger_specs.get_module_manager(Config.DEFAULT_PLANE, Config.DEFAULT_SWAGGER_MODULE)
        rp = module_manager.get_openapi_resource_provider(Config.DEFAULT_RESOURCE_PROVIDER)

        resource_map = rp.get_resource_map_by_tag(swagger_tag)
        if not resource_map:
            raise InvalidAPIUsage(f"Tag `{swagger_tag}` is not exist")

        commands_map = {}
        for resource_id, version_map in resource_map.items():
            v_list = [v for v in version_map]
            if len(v_list) > 1:
                raise InvalidAPIUsage(f"Tag `{swagger_tag}` contains multiple api versions of one resource", payload={
                    "Resource": resource_id,
                    "versions": v_list,
                })

            v = v_list[0]
            # TODO: handle plane here
            cfg_reader = aaz_specs.load_resource_cfg_reader(Config.DEFAULT_PLANE, resource_id, v)
            if not cfg_reader:
                logger.error(f"Command models not exist in aaz for resource: {resource_id} version: {v}")
                continue
            for cmd_names, command in cfg_reader.iter_commands():
                key = tuple(cmd_names)
                if key in commands_map and commands_map[key] != command.version:
                    raise ValueError(f"Multi version contained for command: {''.join(cmd_names)} versions: {commands_map[key]}, {command.version}")
                commands_map[key] = command.version

        profile = _build_profile(profile, commands_map)

        if cli_path is not None:
            assert Config.CLI_PATH is not None
            manager = AzMainManager()
        else:
            assert cli_extension_path is not None
            assert Config.CLI_EXTENSION_PATH is not None
            manager = AzExtensionManager()

        if not manager.has_module(extension_or_module_name):
            logger.info(f"Create cli module `{extension_or_module_name}`")
            manager.create_new_mod(extension_or_module_name)

        logger.info(f"Load cli module `{extension_or_module_name}`")
        module = manager.load_module(extension_or_module_name)

        module.profiles[profile.name] = profile
        logger.info(f"Regenerate module `{extension_or_module_name}`")
        manager.update_module(extension_or_module_name, module.profiles)

    except InvalidAPIUsage as err:
        logger.error(err)
        sys.exit(1)
    except ValueError as err:
        logger.error(err)
        sys.exit(1)


def _build_profile(profile_name, commands_map):
    from cli.model.view import CLIViewProfile, CLIViewCommand, CLIViewCommandGroup
    profile = CLIViewProfile({
        "name": profile_name,
        "commandGroups": {},
    })
    command_group_map = {tuple(): profile}
    for cmd_names, version in commands_map.items():
        group_names = cmd_names[:-1]
        if group_names not in command_group_map:
            group = CLIViewCommandGroup({
                "names": list(group_names),
                "commandGroups": {},
                "commands": {}
            })
        else:
            group = command_group_map[group_names]
        group.commands[cmd_names[-1]] = CLIViewCommand({
            "names": list(cmd_names),
            "version": version,
            "registered": True
        })

        while group_names not in command_group_map:
            command_group_map[group_names] = group
            parent_group_names = group_names[:-1]
            if parent_group_names not in command_group_map:
                parent_group = CLIViewCommandGroup({
                    "names": list(parent_group_names),
                    "commandGroups": {},
                    "commands": {}
                })
            else:
                parent_group = command_group_map[parent_group_names]
            parent_group.command_groups[group_names[-1]] = group

            group = parent_group
            group_names = parent_group_names

    return profile


@bp.cli.command("generate-powershell", short_help="Generate powershell code based on selected azure cli module.")
@click.option(
    "--aaz-path", '-a',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    default=Config.AAZ_PATH,
    required=not Config.AAZ_PATH,
    callback=Config.validate_and_setup_aaz_path,
    expose_value=False,
    help="The local path of aaz repo."
)
@click.option(
    "--cli-path", '-c',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    callback=Config.validate_and_setup_cli_path,
    help="The local path of azure-cli repo. Only required when generate from azure-cli module."
)
@click.option(
    "--cli-extension-path", '-e',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    callback=Config.validate_and_setup_cli_extension_path,
    help="The local path of azure-cli-extension repo. Only required when generate from azure-cli extension."
)
@click.option(
    "--powershell-path", '-p',
    type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    required=True,
    help="The local path of azure-powershell repo."
)
@click.option(
    "--extension-or-module-name", '--name',
    required=True,
    help="Name of the module in azure-cli or the extension in azure-cli-extensions"
)
@click.option(
    "--swagger-path", '-s',
    type=click.Path(file_okay=False, dir_okay=True, readable=True, resolve_path=True),
    default=Config.SWAGGER_PATH,
    required=not Config.SWAGGER_PATH,
    callback=Config.validate_and_setup_swagger_path,
    expose_value=False,
    help="The local path of azure-rest-api-specs repo. Official repo is https://github.com/Azure/azure-rest-api-specs"
)
def generate_powershell(extension_or_module_name, cli_path=None, cli_extension_path=None, powershell_path=None):
    from cli.controller.ps_config_generator import PSAutoRestConfigurationGenerator
    from cli.controller.az_module_manager import AzMainManager, AzExtensionManager
    from cli.templates import get_templates

    # Module path in azure-powershell repo
    
    powershell_path = os.path.join(powershell_path, "src")
    if not os.path.exists(powershell_path):
        logger.error(f"Path `{powershell_path}` not exist")
        sys.exit(1)

    if cli_path is not None:
        assert Config.CLI_PATH is not None
        manager = AzMainManager()
    else:
        assert cli_extension_path is not None
        assert Config.CLI_EXTENSION_PATH is not None
        manager = AzExtensionManager()

    if not manager.has_module(extension_or_module_name):
        logger.error(f"Cannot find module or extension `{extension_or_module_name}`")
        sys.exit(1)
    
    # generate README.md for powershell from CLI, ex, for Oracle, README.md should be generated in src/Oracle/Oracle.Autorest/README.md in azure-powershell repo
    ps_generator = PSAutoRestConfigurationGenerator(manager, extension_or_module_name)
    ps_cfg = ps_generator.generate_config()

    autorest_module_path = os.path.join(powershell_path, ps_cfg.module_name, f"{ps_cfg.module_name}.Autorest")
    if not os.path.exists(autorest_module_path):
        os.makedirs(autorest_module_path)
    readme_file = os.path.join(autorest_module_path, "README.md")
    if os.path.exists(readme_file):
        # read until to the "### AutoRest Configuration"
        with open(readme_file, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith("### AutoRest Configuration"):
                    lines = lines[:i]
                    break
    else:
        lines = []
    
    tmpl = get_templates()['powershell']['configuration']
    data = tmpl.render(cfg=ps_cfg)
    lines.append(data)
    with open(readme_file, "w") as f:
        f.writelines(lines)

    print(f"Generated {readme_file}")
    # Generate and build PowerShell module from the README.md file generated above
    print("Start to generate the PowerShell module from the README.md file in " + autorest_module_path)

    # Execute autorest to generate the PowerShell module
    original_cwd = os.getcwd()
    os.chdir(autorest_module_path)
    exit_code = os.system("pwsh -Command autorest")

     # Print the output of the generation
    if (exit_code != 0):
        print("Failed to generate the module")
        os.chdir(original_cwd)
        sys.exit(1)
    else:
        print("Code generation succeeded.")
        # print(result.stdout)

    os.chdir(original_cwd)
    # Execute autorest to generate the PowerShell module
    print("Start to build the generated PowerShell module")
    result = subprocess.run(
        ["pwsh", "-File", 'build-module.ps1'],
        capture_output=True,
        text=True,
        cwd=autorest_module_path
    )

    if (result.returncode != 0):
        print("Failed to build the module, please see following output for details:")
        print(result.stderr)
        sys.exit(1)
    else:
        print("Module build succeeds, and you may run the generated module by executing the following command: `./run-module.ps1` in " + autorest_module_path)
