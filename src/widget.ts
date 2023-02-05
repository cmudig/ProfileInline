// Copyright (c) Will Epperson
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import { setStoreModels } from './stores';
import { MODULE_NAME, MODULE_VERSION } from './version';
import Widget from './Widget.svelte'

export class VizualizerModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: VizualizerModel.model_name,
      _model_module: VizualizerModel.model_module,
      _model_module_version: VizualizerModel.model_module_version,
      _view_name: VizualizerModel.view_name,
      _view_module: VizualizerModel.view_module,
      _view_module_version: VizualizerModel.view_module_version,
      dfProfile: {}
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'VizualizerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'VizualizerView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class VizualizerView extends DOMWidgetView {
  render() {
    console.log("Rendering VisualizerView")
    setStoreModels(this.model);
    new Widget({ target: this.el });
  }

  // TODO figure out how to add a cell here?

  // public addCell(kind: 'code' | 'markdown', text: string) {
  //   if (this.notebook) {
  //     this.notebook.addCell(kind, text);
  //   }
  // }
}
