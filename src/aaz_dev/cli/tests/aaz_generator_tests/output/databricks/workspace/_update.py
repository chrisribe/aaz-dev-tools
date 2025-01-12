# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "databricks workspace update",
    is_preview=True,
)
class Update(AAZCommand):
    """Update the workspace.

    :example: Update the workspace's tags.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --tags {key1:value1,key2:value2}

    :example: Clean the workspace's tags.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --tags {}

    :example: Prepare for CMK encryption by assigning identity for storage account.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --prepare-encryption

    :example: Configure CMK encryption.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --key-source Microsoft.KeyVault -key-name MyKey --key-vault https://myKeyVault.vault.azure.net/ --key-version 00000000000000000000000000000000

    :example: Revert encryption to Microsoft Managed Keys.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --key-source Default
    """

    _aaz_info = {
        "version": "2018-04-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.databricks/workspaces/{}", "2018-04-01"],
        ]
    }

    AZ_SUPPORT_GENERIC_UPDATE = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.workspace_name = AAZStrArg(
            options=["--workspace-name", "--name", "-n"],
            help="The name of the workspace.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                max_length=64,
                min_length=3,
            ),
        )
        _args_schema.authorizations = AAZListArg(
            options=["--authorizations"],
            singular_options=["--authorization"],
            help="The workspace provider authorizations.",
        )
        _args_schema.managed_resource_group_id = AAZStrArg(
            options=["--managed-resource-group-id"],
            help="The managed resource group Id.",
            required=True,
        )
        _args_schema.parameters = AAZObjectArg(
            options=["--parameters"],
            help="The workspace's custom parameters.",
        )
        _args_schema.ui_definition_uri = AAZStrArg(
            options=["--ui-definition-uri"],
            help="The blob URI where the UI definition file is located.",
        )
        _args_schema.sku = AAZObjectArg(
            options=["--sku"],
            help="The SKU of the resource.",
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            help="Resource tags.",
        )

        authorizations = cls._args_schema.authorizations
        authorizations.Element = AAZObjectArg()

        _element = cls._args_schema.authorizations.Element
        _element.principal_id = AAZUuidArg(
            options=["principal-id"],
            help="The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources.",
            required=True,
        )
        _element.role_definition_id = AAZUuidArg(
            options=["role-definition-id"],
            help="The provider's role definition identifier. This role will define all the permissions that the provider must have on the workspace's container resource group. This role definition cannot have permission to delete the resource group.",
            required=True,
        )

        parameters = cls._args_schema.parameters
        parameters.aml_workspace_id = AAZObjectArg(
            options=["aml-workspace-id"],
            help="The ID of a Azure Machine Learning workspace to link with Databricks workspace",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.aml_workspace_id)
        parameters.custom_private_subnet_name = AAZObjectArg(
            options=["custom-private-subnet-name"],
            help="The name of the Private Subnet within the Virtual Network",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.custom_private_subnet_name)
        parameters.custom_public_subnet_name = AAZObjectArg(
            options=["custom-public-subnet-name"],
            help="The name of a Public Subnet within the Virtual Network",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.custom_public_subnet_name)
        parameters.custom_virtual_network_id = AAZObjectArg(
            options=["custom-virtual-network-id"],
            help="The ID of a Virtual Network where this Databricks Cluster should be created",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.custom_virtual_network_id)
        parameters.enable_no_public_ip = AAZObjectArg(
            options=["enable-no-public-ip"],
            help="Should the Public IP be Disabled?",
        )
        cls._build_args_workspace_custom_boolean_parameter_update(parameters.enable_no_public_ip)
        parameters.encryption = AAZObjectArg(
            options=["encryption"],
            help="Contains the encryption details for Customer-Managed Key (CMK) enabled workspace.",
        )
        parameters.load_balancer_backend_pool_name = AAZObjectArg(
            options=["load-balancer-backend-pool-name"],
            help="Name of the outbound Load Balancer Backend Pool for Secure Cluster Connectivity (No Public IP).",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.load_balancer_backend_pool_name)
        parameters.load_balancer_id = AAZObjectArg(
            options=["load-balancer-id"],
            help="Resource URI of Outbound Load balancer for Secure Cluster Connectivity (No Public IP) workspace.",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.load_balancer_id)
        parameters.nat_gateway_name = AAZObjectArg(
            options=["nat-gateway-name"],
            help="Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets.",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.nat_gateway_name)
        parameters.prepare_encryption = AAZObjectArg(
            options=["prepare-encryption"],
            help="Prepare the workspace for encryption. Enables the Managed Identity for managed storage account.",
        )
        cls._build_args_workspace_custom_boolean_parameter_update(parameters.prepare_encryption)
        parameters.public_ip_name = AAZObjectArg(
            options=["public-ip-name"],
            help="Name of the Public IP for No Public IP workspace with managed vNet.",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.public_ip_name)
        parameters.require_infrastructure_encryption = AAZObjectArg(
            options=["require-infrastructure-encryption"],
            help="A boolean indicating whether or not the DBFS root file system will be enabled with secondary layer of encryption with platform managed keys for data at rest.",
        )
        cls._build_args_workspace_custom_boolean_parameter_update(parameters.require_infrastructure_encryption)
        parameters.storage_account_name = AAZObjectArg(
            options=["storage-account-name"],
            help="Default DBFS storage account name.",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.storage_account_name)
        parameters.storage_account_sku_name = AAZObjectArg(
            options=["storage-account-sku-name"],
            help="Storage account SKU name, ex: Standard_GRS, Standard_LRS. Refer https://aka.ms/storageskus for valid inputs.",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.storage_account_sku_name)
        parameters.vnet_address_prefix = AAZObjectArg(
            options=["vnet-address-prefix"],
            help="Address prefix for Managed virtual network. Default value for this input is 10.139.",
        )
        cls._build_args_workspace_custom_string_parameter_update(parameters.vnet_address_prefix)

        encryption = cls._args_schema.parameters.encryption
        encryption.value = AAZObjectArg(
            options=["value"],
            help="The value which should be used for this field.",
        )

        value = cls._args_schema.parameters.encryption.value
        value.key_name = AAZStrArg(
            options=["key-name"],
            help="The name of KeyVault key.",
        )
        value.key_source = AAZStrArg(
            options=["key-source"],
            help="The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault",
            default="Default",
            enum={"Default": "Default", "Microsoft.Keyvault": "Microsoft.Keyvault"},
        )
        value.keyvaulturi = AAZStrArg(
            options=["keyvaulturi"],
            help="The Uri of KeyVault.",
        )
        value.keyversion = AAZStrArg(
            options=["keyversion"],
            help="The version of KeyVault key.",
        )

        sku = cls._args_schema.sku
        sku.name = AAZStrArg(
            options=["name"],
            help="The SKU name.",
            required=True,
        )
        sku.tier = AAZStrArg(
            options=["tier"],
            help="The SKU tier.",
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg()
        return cls._args_schema

    _args_workspace_custom_boolean_parameter_update = None

    @classmethod
    def _build_args_workspace_custom_boolean_parameter_update(cls, _schema):
        if cls._args_workspace_custom_boolean_parameter_update is not None:
            _schema.value = cls._args_workspace_custom_boolean_parameter_update.value
            return

        cls._args_workspace_custom_boolean_parameter_update = AAZObjectArg()

        workspace_custom_boolean_parameter_update = cls._args_workspace_custom_boolean_parameter_update
        workspace_custom_boolean_parameter_update.value = AAZBoolArg(
            options=["value"],
            help="The value which should be used for this field.",
            required=True,
        )

        _schema.value = cls._args_workspace_custom_boolean_parameter_update.value

    _args_workspace_custom_string_parameter_update = None

    @classmethod
    def _build_args_workspace_custom_string_parameter_update(cls, _schema):
        if cls._args_workspace_custom_string_parameter_update is not None:
            _schema.value = cls._args_workspace_custom_string_parameter_update.value
            return

        cls._args_workspace_custom_string_parameter_update = AAZObjectArg()

        workspace_custom_string_parameter_update = cls._args_workspace_custom_string_parameter_update
        workspace_custom_string_parameter_update.value = AAZStrArg(
            options=["value"],
            help="The value which should be used for this field.",
            required=True,
        )

        _schema.value = cls._args_workspace_custom_string_parameter_update.value

    def _execute_operations(self):
        self.pre_operations()
        self.WorkspacesGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.WorkspacesCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    @register_callback
    def pre_instance_update(self, instance):
        pass

    @register_callback
    def post_instance_update(self, instance):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class WorkspacesGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.workspace_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2018-04-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _UpdateHelper._build_schema_workspace_read(cls._schema_on_200)

            return cls._schema_on_200

    class WorkspacesCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    False,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    False,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.workspace_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2018-04-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=self.ctx.vars.instance,
            )

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()
            _UpdateHelper._build_schema_workspace_read(cls._schema_on_200_201)

            return cls._schema_on_200_201

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})
            _builder.set_prop("sku", AAZObjectType, ".sku")
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("authorizations", AAZListType, ".authorizations")
                properties.set_prop("managedResourceGroupId", AAZStrType, ".managed_resource_group_id", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("parameters", AAZObjectType, ".parameters")
                properties.set_prop("uiDefinitionUri", AAZStrType, ".ui_definition_uri")

            authorizations = _builder.get(".properties.authorizations")
            if authorizations is not None:
                authorizations.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.authorizations[]")
            if _elements is not None:
                _elements.set_prop("principalId", AAZStrType, ".principal_id", typ_kwargs={"flags": {"required": True}})
                _elements.set_prop("roleDefinitionId", AAZStrType, ".role_definition_id", typ_kwargs={"flags": {"required": True}})

            parameters = _builder.get(".properties.parameters")
            if parameters is not None:
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("amlWorkspaceId", AAZObjectType, ".aml_workspace_id"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("customPrivateSubnetName", AAZObjectType, ".custom_private_subnet_name"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("customPublicSubnetName", AAZObjectType, ".custom_public_subnet_name"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("customVirtualNetworkId", AAZObjectType, ".custom_virtual_network_id"))
                _UpdateHelper._build_schema_workspace_custom_boolean_parameter_update(parameters.set_prop("enableNoPublicIp", AAZObjectType, ".enable_no_public_ip"))
                parameters.set_prop("encryption", AAZObjectType, ".encryption")
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("loadBalancerBackendPoolName", AAZObjectType, ".load_balancer_backend_pool_name"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("loadBalancerId", AAZObjectType, ".load_balancer_id"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("natGatewayName", AAZObjectType, ".nat_gateway_name"))
                _UpdateHelper._build_schema_workspace_custom_boolean_parameter_update(parameters.set_prop("prepareEncryption", AAZObjectType, ".prepare_encryption"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("publicIpName", AAZObjectType, ".public_ip_name"))
                _UpdateHelper._build_schema_workspace_custom_boolean_parameter_update(parameters.set_prop("requireInfrastructureEncryption", AAZObjectType, ".require_infrastructure_encryption"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("storageAccountName", AAZObjectType, ".storage_account_name"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("storageAccountSkuName", AAZObjectType, ".storage_account_sku_name"))
                _UpdateHelper._build_schema_workspace_custom_string_parameter_update(parameters.set_prop("vnetAddressPrefix", AAZObjectType, ".vnet_address_prefix"))

            encryption = _builder.get(".properties.parameters.encryption")
            if encryption is not None:
                encryption.set_prop("value", AAZObjectType, ".value")

            value = _builder.get(".properties.parameters.encryption.value")
            if value is not None:
                value.set_prop("KeyName", AAZStrType, ".key_name")
                value.set_prop("keySource", AAZStrType, ".key_source")
                value.set_prop("keyvaulturi", AAZStrType, ".keyvaulturi")
                value.set_prop("keyversion", AAZStrType, ".keyversion")

            sku = _builder.get(".sku")
            if sku is not None:
                sku.set_prop("name", AAZStrType, ".name", typ_kwargs={"flags": {"required": True}})
                sku.set_prop("tier", AAZStrType, ".tier")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


class _UpdateHelper:
    """Helper class for Update"""

    @classmethod
    def _build_schema_workspace_custom_boolean_parameter_update(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("value", AAZBoolType, ".value", typ_kwargs={"flags": {"required": True}})

    @classmethod
    def _build_schema_workspace_custom_string_parameter_update(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("value", AAZStrType, ".value", typ_kwargs={"flags": {"required": True}})

    _schema_created_by_read = None

    @classmethod
    def _build_schema_created_by_read(cls, _schema):
        if cls._schema_created_by_read is not None:
            _schema.application_id = cls._schema_created_by_read.application_id
            _schema.oid = cls._schema_created_by_read.oid
            _schema.puid = cls._schema_created_by_read.puid
            return

        cls._schema_created_by_read = _schema_created_by_read = AAZObjectType()

        created_by_read = _schema_created_by_read
        created_by_read.application_id = AAZStrType(
            serialized_name="applicationId",
            flags={"read_only": True},
        )
        created_by_read.oid = AAZStrType(
            flags={"read_only": True},
        )
        created_by_read.puid = AAZStrType(
            flags={"read_only": True},
        )

        _schema.application_id = cls._schema_created_by_read.application_id
        _schema.oid = cls._schema_created_by_read.oid
        _schema.puid = cls._schema_created_by_read.puid

    _schema_workspace_custom_boolean_parameter_read = None

    @classmethod
    def _build_schema_workspace_custom_boolean_parameter_read(cls, _schema):
        if cls._schema_workspace_custom_boolean_parameter_read is not None:
            _schema.type = cls._schema_workspace_custom_boolean_parameter_read.type
            _schema.value = cls._schema_workspace_custom_boolean_parameter_read.value
            return

        cls._schema_workspace_custom_boolean_parameter_read = _schema_workspace_custom_boolean_parameter_read = AAZObjectType()

        workspace_custom_boolean_parameter_read = _schema_workspace_custom_boolean_parameter_read
        workspace_custom_boolean_parameter_read.type = AAZStrType(
            flags={"read_only": True},
        )
        workspace_custom_boolean_parameter_read.value = AAZBoolType(
            flags={"required": True},
        )

        _schema.type = cls._schema_workspace_custom_boolean_parameter_read.type
        _schema.value = cls._schema_workspace_custom_boolean_parameter_read.value

    _schema_workspace_custom_string_parameter_read = None

    @classmethod
    def _build_schema_workspace_custom_string_parameter_read(cls, _schema):
        if cls._schema_workspace_custom_string_parameter_read is not None:
            _schema.type = cls._schema_workspace_custom_string_parameter_read.type
            _schema.value = cls._schema_workspace_custom_string_parameter_read.value
            return

        cls._schema_workspace_custom_string_parameter_read = _schema_workspace_custom_string_parameter_read = AAZObjectType()

        workspace_custom_string_parameter_read = _schema_workspace_custom_string_parameter_read
        workspace_custom_string_parameter_read.type = AAZStrType(
            flags={"read_only": True},
        )
        workspace_custom_string_parameter_read.value = AAZStrType(
            flags={"required": True},
        )

        _schema.type = cls._schema_workspace_custom_string_parameter_read.type
        _schema.value = cls._schema_workspace_custom_string_parameter_read.value

    _schema_workspace_read = None

    @classmethod
    def _build_schema_workspace_read(cls, _schema):
        if cls._schema_workspace_read is not None:
            _schema.id = cls._schema_workspace_read.id
            _schema.location = cls._schema_workspace_read.location
            _schema.name = cls._schema_workspace_read.name
            _schema.properties = cls._schema_workspace_read.properties
            _schema.sku = cls._schema_workspace_read.sku
            _schema.tags = cls._schema_workspace_read.tags
            _schema.type = cls._schema_workspace_read.type
            return

        cls._schema_workspace_read = _schema_workspace_read = AAZObjectType()

        workspace_read = _schema_workspace_read
        workspace_read.id = AAZStrType(
            flags={"read_only": True},
        )
        workspace_read.location = AAZStrType(
            flags={"required": True},
        )
        workspace_read.name = AAZStrType(
            flags={"read_only": True},
        )
        workspace_read.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )
        workspace_read.sku = AAZObjectType()
        workspace_read.tags = AAZDictType()
        workspace_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_workspace_read.properties
        properties.authorizations = AAZListType()
        properties.created_by = AAZObjectType(
            serialized_name="createdBy",
        )
        cls._build_schema_created_by_read(properties.created_by)
        properties.created_date_time = AAZStrType(
            serialized_name="createdDateTime",
            flags={"read_only": True},
        )
        properties.managed_resource_group_id = AAZStrType(
            serialized_name="managedResourceGroupId",
            flags={"required": True},
        )
        properties.parameters = AAZObjectType()
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.storage_account_identity = AAZObjectType(
            serialized_name="storageAccountIdentity",
        )
        properties.ui_definition_uri = AAZStrType(
            serialized_name="uiDefinitionUri",
        )
        properties.updated_by = AAZObjectType(
            serialized_name="updatedBy",
        )
        cls._build_schema_created_by_read(properties.updated_by)
        properties.workspace_id = AAZStrType(
            serialized_name="workspaceId",
            flags={"read_only": True},
        )
        properties.workspace_url = AAZStrType(
            serialized_name="workspaceUrl",
            flags={"read_only": True},
        )

        authorizations = _schema_workspace_read.properties.authorizations
        authorizations.Element = AAZObjectType()

        _element = _schema_workspace_read.properties.authorizations.Element
        _element.principal_id = AAZStrType(
            serialized_name="principalId",
            flags={"required": True},
        )
        _element.role_definition_id = AAZStrType(
            serialized_name="roleDefinitionId",
            flags={"required": True},
        )

        parameters = _schema_workspace_read.properties.parameters
        parameters.aml_workspace_id = AAZObjectType(
            serialized_name="amlWorkspaceId",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.aml_workspace_id)
        parameters.custom_private_subnet_name = AAZObjectType(
            serialized_name="customPrivateSubnetName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.custom_private_subnet_name)
        parameters.custom_public_subnet_name = AAZObjectType(
            serialized_name="customPublicSubnetName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.custom_public_subnet_name)
        parameters.custom_virtual_network_id = AAZObjectType(
            serialized_name="customVirtualNetworkId",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.custom_virtual_network_id)
        parameters.enable_no_public_ip = AAZObjectType(
            serialized_name="enableNoPublicIp",
        )
        cls._build_schema_workspace_custom_boolean_parameter_read(parameters.enable_no_public_ip)
        parameters.encryption = AAZObjectType()
        parameters.load_balancer_backend_pool_name = AAZObjectType(
            serialized_name="loadBalancerBackendPoolName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.load_balancer_backend_pool_name)
        parameters.load_balancer_id = AAZObjectType(
            serialized_name="loadBalancerId",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.load_balancer_id)
        parameters.nat_gateway_name = AAZObjectType(
            serialized_name="natGatewayName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.nat_gateway_name)
        parameters.prepare_encryption = AAZObjectType(
            serialized_name="prepareEncryption",
        )
        cls._build_schema_workspace_custom_boolean_parameter_read(parameters.prepare_encryption)
        parameters.public_ip_name = AAZObjectType(
            serialized_name="publicIpName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.public_ip_name)
        parameters.require_infrastructure_encryption = AAZObjectType(
            serialized_name="requireInfrastructureEncryption",
        )
        cls._build_schema_workspace_custom_boolean_parameter_read(parameters.require_infrastructure_encryption)
        parameters.resource_tags = AAZObjectType(
            serialized_name="resourceTags",
            flags={"read_only": True},
        )
        parameters.storage_account_name = AAZObjectType(
            serialized_name="storageAccountName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.storage_account_name)
        parameters.storage_account_sku_name = AAZObjectType(
            serialized_name="storageAccountSkuName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.storage_account_sku_name)
        parameters.vnet_address_prefix = AAZObjectType(
            serialized_name="vnetAddressPrefix",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.vnet_address_prefix)

        encryption = _schema_workspace_read.properties.parameters.encryption
        encryption.type = AAZStrType(
            flags={"read_only": True},
        )
        encryption.value = AAZObjectType()

        value = _schema_workspace_read.properties.parameters.encryption.value
        value.key_name = AAZStrType(
            serialized_name="KeyName",
        )
        value.key_source = AAZStrType(
            serialized_name="keySource",
        )
        value.keyvaulturi = AAZStrType()
        value.keyversion = AAZStrType()

        resource_tags = _schema_workspace_read.properties.parameters.resource_tags
        resource_tags.type = AAZStrType(
            flags={"read_only": True},
        )
        resource_tags.value = AAZFreeFormDictType(
            flags={"required": True, "read_only": True},
        )

        storage_account_identity = _schema_workspace_read.properties.storage_account_identity
        storage_account_identity.principal_id = AAZStrType(
            serialized_name="principalId",
            flags={"read_only": True},
        )
        storage_account_identity.tenant_id = AAZStrType(
            serialized_name="tenantId",
            flags={"read_only": True},
        )
        storage_account_identity.type = AAZStrType(
            flags={"read_only": True},
        )

        sku = _schema_workspace_read.sku
        sku.name = AAZStrType(
            flags={"required": True},
        )
        sku.tier = AAZStrType()

        tags = _schema_workspace_read.tags
        tags.Element = AAZStrType()

        _schema.id = cls._schema_workspace_read.id
        _schema.location = cls._schema_workspace_read.location
        _schema.name = cls._schema_workspace_read.name
        _schema.properties = cls._schema_workspace_read.properties
        _schema.sku = cls._schema_workspace_read.sku
        _schema.tags = cls._schema_workspace_read.tags
        _schema.type = cls._schema_workspace_read.type


__all__ = ["Update"]
