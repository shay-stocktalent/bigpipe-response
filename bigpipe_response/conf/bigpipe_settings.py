import os

import hydra
from omegaconf import OmegaConf
from pkg_resources import resource_exists

from bigpipe_response.exceptions import InvalidConfiguration
from bigpipe_response.javascript_dom_bind.javascript_dom_bind import JavascriptDOMBind
from bigpipe_response.processors.remote_js_processor import RemoteJsProcessor


class BigpipeSettings:
    @staticmethod
    def validate_settings(config):
        js_source_path = OmegaConf.to_container(config.processors.js.source_path, resolve=True)
        css_source_path = OmegaConf.to_container(config.processors.css.source_path, resolve=True)

        if js_source_path and not isinstance(js_source_path, list):
            raise InvalidConfiguration('js_source_path must be supplied as list')

        for source_base_path in js_source_path:
            if not os.path.exists(source_base_path):
                raise InvalidConfiguration('js_source_path directory dose not exists. [{}]'.format(source_base_path))

        if css_source_path and not isinstance(css_source_path, list):
            raise InvalidConfiguration('js_source_path must be supplied as list')

        for source_base_path in css_source_path:
            if not os.path.exists(source_base_path):
                raise InvalidConfiguration('css_source_path directory dose not exists. [{}]'.format(source_base_path))

        if not config.rendered_output_path or not os.path.isdir(config.rendered_output_path):
            raise InvalidConfiguration('rendered_output_path need to be a an exists path')

        if not isinstance(config.is_production_mode, bool):
            raise InvalidConfiguration('is_production_mode must be of type boolean')

        if not config.processors.js.name:
            raise InvalidConfiguration('processors.js.name must be set')

        if not config.processors.js.source_ext or not isinstance(
            OmegaConf.to_container(config.processors.js.source_ext, resolve=True), list
        ):
            raise InvalidConfiguration('config.processors.js.source_ext must be a populated list')

        if not config.processors.js.target_ext:
            raise InvalidConfiguration('config.processors.js.target_ext must be set')

        if not config.processors.js.javascript_handler.strip().lower().endswith('.js'):
            raise InvalidConfiguration('js_processor_handler_path must be with js extension.')

        if not config.processors.js.javascript_handler:
            raise InvalidConfiguration('config.processors.js.javascript_handler must be set')

        path, resource = RemoteJsProcessor.build_js_resource(config.processors.js.javascript_handler)
        if not resource_exists(path, resource):
            raise InvalidConfiguration('js_processor_handler_path must be set to a javascript file')

        if JavascriptDOMBind not in hydra.utils.get_class(config.processors.js.javascript_dom_bind).__bases__:
            raise InvalidConfiguration('config.processors.js.javascript_dom_bind must be set and instance of JavascriptDOMBind')

        if not config.processors.js.remote_port_start:
            raise InvalidConfiguration('config.processors.js.remote_port_start must be set to a port number')

        if not config.processors.js.remote_port_count:
            raise InvalidConfiguration('config.processors.js.remote_port_count must be set to number of ports to scan')

        if not config.processors.css.name:
            raise InvalidConfiguration('config.processors.css.name must be set')

        if not config.processors.css.source_ext or not isinstance(OmegaConf.to_container(config.processors.css.source_ext, resolve=True), list):
            raise InvalidConfiguration('processor.css.source_ext must be a populated list')

        if not config.processors.css.target_ext:
            raise InvalidConfiguration('config.processors.css.target_ext must be set')

        if config.processors.css.complete_dependencies_by_js is None:
            raise InvalidConfiguration('config.processors.css.complete_dependencies_by_js must be set to boolean')

        if config.processors.css.bundle_link_dependencies is None:
            raise InvalidConfiguration('config.processors.css.bundle_link_dependencies must be set to boolean')

        if not config.processors.i18n.name:
            raise InvalidConfiguration('i18n_processor_name must be set')
