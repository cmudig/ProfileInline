import type { Writable } from 'svelte/store';
import type { DOMWidgetModel } from '@jupyter-widgets/base';
import { writable } from 'svelte/store';

import type { IDFProfileWState } from './common/exchangeInterfaces'

interface WidgetWritable<T> extends Writable<T> {
  setModel: (m: DOMWidgetModel) => void;
}

export function WidgetWritable<T>(name_: string, value_: T): WidgetWritable<T> {
  const name: string = name_;
  const internalWritable: Writable<any> = writable(value_);
  let model: DOMWidgetModel;

  return {
    set: (v: any) => {
      internalWritable.set(v);
      if (model) {
        model.set(name, v);
        model.save_changes();
      }
    },
    subscribe: internalWritable.subscribe,
    update: (func: any) => {
      internalWritable.update((v: any) => {
        const output = func(v);
        if (model) {
          model.set(name, output);
          model.save_changes();
        }
        return output;
      });
    },
    setModel: (m: DOMWidgetModel) => {
      model = m;
      const modelValue = model.get(name);
      if (modelValue) {
        internalWritable.set(modelValue);
      }

      model.on(
        'change:' + name,
        () => internalWritable.set(model.get(name)),
        null
      );
    },
  };
}

// Declare stores with their associated Traitlets here.
export const dfProfile = WidgetWritable<IDFProfileWState>('dfProfile', {
  profile: [],
  shape: [0, 0],
  dfName: 'test',
  lastUpdatedTime: 0,
  isPinned: false,
  warnings: [],
});


// Set the model for each store you create.
export function setStoreModels(model: DOMWidgetModel): void {
  dfProfile.setModel(model);
}
