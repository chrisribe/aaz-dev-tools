from swagger.tests.common import SwaggerSpecsTestCase
from swagger.controller.command_generator import CommandGenerator
from swagger.model.specs._utils import get_url_path_valid_parts
from command.model.configuration import CMDResource
from swagger.utils import exceptions

MUTE_ERROR_MESSAGES = (
    "type is not supported",
    "format is not supported"
)


class CommandGeneratorTest(SwaggerSpecsTestCase):

    def test_monitor_control_service(self):
        rp = next(self.get_mgmt_plane_resource_providers(
                module_filter=lambda m: m.name == "monitor",
                resource_provider_filter=lambda r: r.name == "Microsoft.Insights"
        ))

        v = "2021-04-01"
        generator = CommandGenerator(module_name=str(rp.swagger_module))

        resource_map = rp.get_resource_map(read_only=True)
        resource_ids = []
        resource_versions = set()
        for r_id, r_version_map in resource_map.items():
            resource_ids.append(r_id)
            resource_versions.update(r_version_map.keys())

        for r_id in resource_ids:
            if v in resource_map[r_id]:
                cmd_resource = CMDResource({
                    "id": r_id,
                    "version": str(v)
                })
                try:
                    resources = generator.load_resources([cmd_resource])
                    generator.create_draft_command_group(resources[r_id])
                except exceptions.InvalidSwaggerValueError as err:
                    if err.msg not in MUTE_ERROR_MESSAGES:
                        print(err)
                except Exception:
                    print(resource_map[r_id][v])
                    raise

    def test_data_factory_integration_runtimes(self):
        rp = next(self.get_mgmt_plane_resource_providers(
            module_filter=lambda m: m.name == "datafactory",
            resource_provider_filter=lambda r: r.name == "Microsoft.DataFactory"
        ))

        v = "2018-06-01"
        generator = CommandGenerator(module_name=str(rp.swagger_module))

        resource_map = rp.get_resource_map(read_only=True)
        resource_ids = []
        resource_versions = set()
        for r_id, r_version_map in resource_map.items():
            resource_ids.append(r_id)
            resource_versions.update(r_version_map.keys())

        for r_id in resource_ids:
            if v in resource_map[r_id]:
                cmd_resource = CMDResource({
                    "id": r_id,
                    "version": str(v)
                })
                try:
                    resources = generator.load_resources([cmd_resource])
                    generator.create_draft_command_group(resources[r_id])
                except exceptions.InvalidSwaggerValueError as err:
                    if err.msg not in MUTE_ERROR_MESSAGES:
                        print(err)
                except Exception:
                    print(resource_map[r_id][v])
                    raise

    def test_data_factory(self):
        rp = next(self.get_mgmt_plane_resource_providers(
            module_filter=lambda m: m.name == "datafactory",
            resource_provider_filter=lambda r: r.name == "Microsoft.DataFactory"
        ))

        v = "2018-06-01"
        generator = CommandGenerator(module_name=str(rp.swagger_module))

        resource_map = rp.get_resource_map(read_only=True)
        resource_ids = []
        resource_versions = set()
        for r_id, r_version_map in resource_map.items():
            resource_ids.append(r_id)
            resource_versions.update(r_version_map.keys())

        for r_id in resource_ids:
            if v in resource_map[r_id]:
                cmd_resource = CMDResource({
                    "id": r_id,
                    "version": str(v)
                })
                try:
                    resources = generator.load_resources([cmd_resource])
                    generator.create_draft_command_group(resources[r_id])
                except exceptions.InvalidSwaggerValueError as err:
                    if err.msg not in MUTE_ERROR_MESSAGES:
                        print(err)
                except Exception:
                    print(resource_map[r_id][v])
                    raise

    def test_recovery_services(self):
        rp = next(self.get_mgmt_plane_resource_providers(
            module_filter=lambda m: m.name == "recoveryservicessiterecovery",
            resource_provider_filter=lambda r: r.name == "Microsoft.RecoveryServices"
        ))

        generator = CommandGenerator(module_name=str(rp.swagger_module))

        resource_map = rp.get_resource_map(read_only=True)
        resource_ids = []
        resource_versions = set()
        for r_id, r_version_map in resource_map.items():
            resource_ids.append(r_id)
            resource_versions.update(r_version_map.keys())

        for r_id in resource_ids:
            for v in resource_versions:
                if v in resource_map[r_id]:
                    cmd_resource = CMDResource({
                        "id": r_id,
                        "version": str(v)
                    })
                    try:
                        resources = generator.load_resources([cmd_resource])
                        generator.create_draft_command_group(resources[r_id])
                    except exceptions.InvalidSwaggerValueError as err:
                        if err.msg not in MUTE_ERROR_MESSAGES:
                            print(err)
                    except Exception:
                        print(resource_map[r_id][v])
                        raise

    def test_databox(self):
        rp = next(self.get_mgmt_plane_resource_providers(
            module_filter=lambda m: m.name == "databox",
            resource_provider_filter=lambda r: r.name == "Microsoft.DataBox"
        ))

        generator = CommandGenerator(module_name=str(rp.swagger_module))

        resource_map = rp.get_resource_map(read_only=True)
        resource_ids = []
        resource_versions = set()
        for r_id, r_version_map in resource_map.items():
            resource_ids.append(r_id)
            resource_versions.update(r_version_map.keys())

        for r_id in resource_ids:
            for v in resource_versions:
                if v in resource_map[r_id]:
                    cmd_resource = CMDResource({
                        "id": r_id,
                        "version": str(v)
                    })
                    try:
                        resources = generator.load_resources([cmd_resource])
                        generator.create_draft_command_group(resources[r_id])
                    except exceptions.InvalidSwaggerValueError as err:
                        if err.msg not in MUTE_ERROR_MESSAGES:
                            print(err)
                    except Exception:
                        print(resource_map[r_id][v])
                        raise

    # def test_securityinsights(self):
    #     rp = next(self.get_mgmt_plane_resource_providers(
    #         module_filter=lambda m: m.name == "securityinsights",
    #         resource_provider_filter=lambda r: r.name == "Microsoft.SecurityInsights"
    #     ))
    #
    #     generator = CommandConfigurationGenerator()
    #
    #     resource_map = rp.get_resource_map(read_only=True)
    #     resource_op_group_map = rp.get_resource_op_group_map(resource_map)
    #     for op_group_name in resource_op_group_map:
    #         versions = set()
    #         for resource_id in resource_op_group_map[op_group_name]:
    #             versions.update(resource_map[resource_id].keys())
    #         for version in versions:
    #             # print(op_group_name, version)
    #             resources = []
    #             for resource_id in resource_op_group_map[op_group_name]:
    #                 if version in resource_map[resource_id]:
    #                     resources.append(resource_map[resource_id][version])
    #             try:
    #                 generator.load_resources(resources)
    #             except exceptions.InvalidSwaggerValueError as err:
    #                 if err.msg not in MUTE_ERROR_MESSAGES:
    #                     print(err)
    #             except Exception:
    #                 print([str(resource) for resource in resources])
    #                 raise

    def test_network(self):
        rp = next(self.get_mgmt_plane_resource_providers(
            module_filter=lambda m: m.name == "network",
            resource_provider_filter=lambda r: r.name == "Microsoft.Network"
        ))
        print(str(rp))

        generator = CommandGenerator(module_name=str(rp.swagger_module))

        resource_map = rp.get_resource_map(read_only=True)
        resource_ids = []
        resource_versions = set()
        for r_id, r_version_map in resource_map.items():
            resource_ids.append(r_id)
            resource_versions.update(r_version_map.keys())

        for r_id in resource_ids:
            for v in resource_versions:
                if v in resource_map[r_id]:
                    cmd_resource = CMDResource({
                        "id": r_id,
                        "version": str(v)
                    })
                    try:
                        resources = generator.load_resources([cmd_resource])
                        generator.create_draft_command_group(resources[r_id])
                    except exceptions.InvalidSwaggerValueError as err:
                        if err.msg not in MUTE_ERROR_MESSAGES:
                            print(err)
                    except Exception:
                        print(resource_map[r_id][v])
                        raise

    def test_mgmt_modules(self):
        # without network module
        for rp in self.get_mgmt_plane_resource_providers(
                module_filter=lambda m: m.name not in (
                        "network",  # Take hours to execute
                        "securityinsights",  # invalid swagger
                ),
                resource_provider_filter=lambda m: str(m) not in (
                        "(MgmtPlane)/azsadmin/infrastructureinsights/Microsoft.InfrastructureInsights.Admin",  # have invalid reference
                )
        ):
            print(str(rp))

            generator = CommandGenerator(module_name=str(rp.swagger_module))

            resource_map = rp.get_resource_map(read_only=True)
            resource_ids = []
            resource_versions = set()
            for r_id, r_version_map in resource_map.items():
                resource_ids.append(r_id)
                resource_versions.update(r_version_map.keys())

            for r_id in resource_ids:
                for v in resource_versions:
                    if v in resource_map[r_id]:
                        cmd_resource = CMDResource({
                                "id": r_id,
                                "version": str(v)
                            })
                        try:
                            resources = generator.load_resources([cmd_resource])
                            generator.create_draft_command_group(resources[r_id])
                        except exceptions.InvalidSwaggerValueError as err:
                            if err.msg not in MUTE_ERROR_MESSAGES:
                                print(err)
                        except Exception:
                            print(resource_map[r_id][v])
                            raise

    def test_data_plane_modules(self):
        for rp in self.get_data_plane_resource_providers(
                resource_provider_filter=lambda m: str(m) not in (
                    "(DataPlane)/cognitiveservices/AutoSuggest",  # have complicated loop reference
                    "(DataPlane)/cognitiveservices/ImageSearch",
                    "(DataPlane)/cognitiveservices/WebSearch"
                )
        ):
            print(str(rp))

            generator = CommandGenerator(module_name=str(rp.swagger_module))

            resource_map = rp.get_resource_map(read_only=True)
            resource_ids = []
            resource_versions = set()
            for r_id, r_version_map in resource_map.items():
                resource_ids.append(r_id)
                resource_versions.update(r_version_map.keys())

            for r_id in resource_ids:
                for v in resource_versions:
                    if v in resource_map[r_id]:
                        cmd_resource = CMDResource({
                            "id": r_id,
                            "version": str(v)
                        })
                        try:
                            resources = generator.load_resources([cmd_resource])
                            generator.create_draft_command_group(resources[r_id])
                        except exceptions.InvalidSwaggerValueError as err:
                            if err.msg not in MUTE_ERROR_MESSAGES:
                                print(err)
                        except Exception:
                            print(resource_map[r_id][v])
                            raise

    def test_command_group_name_mgmt_plane(self):
        for rp in self.get_mgmt_plane_resource_providers():
            print(str(rp))
            command_group_names = {}
            resource_map = rp.get_resource_map(read_only=True)
            for r_id, r_version_map in resource_map.items():
                valid_parts = get_url_path_valid_parts(r_id, rp.name)
                if len(valid_parts) and valid_parts[-1] == '{}':
                    valid_url = '/'.join(valid_parts[:-1])
                else:
                    valid_url = '/'.join(valid_parts)

                for part in valid_parts:
                    if part.lower() == "providers":
                        print(f"Multi providers in valid_parts: {valid_url} :\n\t {r_id}")

                names = set()
                for resource in r_version_map.values():
                    name = CommandGenerator._generate_command_group_name_by_resource(resource)
                    if name and name not in names:
                        names.add(name)
                if len(names) > 1:
                    print(f"Multi Command group names: {resource.path} :\n\t{names}")
                for name in names:
                    if name in command_group_names and command_group_names[name][0] != valid_url:
                        print(f"Duplicated command group name : '{name}' :\n\t{command_group_names[name][0]} and {valid_url} :\n\t\t{command_group_names[name][1]}\n\t\t{resource.path}")
                    command_group_names[name] = (valid_url, resource.path)

    def test_command_group_name_data_plane(self):
        for rp in self.get_data_plane_resource_providers():
            print(str(rp))
            command_group_names = {}
            resource_map = rp.get_resource_map(read_only=True)
            for r_id, r_version_map in resource_map.items():
                valid_parts = get_url_path_valid_parts(r_id, rp.name)
                if len(valid_parts) and valid_parts[-1] == '{}':
                    valid_url = '/'.join(valid_parts[:-1])
                else:
                    valid_url = '/'.join(valid_parts)

                for part in valid_parts:
                    if part.lower() == "providers":
                        print(f"Multi providers in valid_parts: {valid_url} :\n\t {r_id}")

                names = set()
                for resource in r_version_map.values():
                    name = CommandGenerator._generate_command_group_name_by_resource(resource)
                    if name and name not in names:
                        names.add(name)
                if len(names) > 1:
                    print(f"Multi Command group names: {resource.path} :\n\t{names}")
                for name in names:
                    if name in command_group_names and command_group_names[name][0] != valid_url:
                        print(f"Duplicated command group name : '{name}' :\n\t{command_group_names[name][0]} and {valid_url} :\n\t\t{command_group_names[name][1]}\n\t\t{resource.path}")
                    command_group_names[name] = (valid_url, resource.path)