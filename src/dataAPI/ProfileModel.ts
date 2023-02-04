import type { NotebookAPI } from './jupyter/notebook';

import _ from 'lodash';
import type { Logger } from '../logger/Logger';

export class ProfileModel {

    private _notebook: NotebookAPI;
    private _logger;

    constructor() {
    }

    get notebook(): NotebookAPI {
        return this._notebook
    }

    // handle the notebook connection as a traillet or something


    get logger(): Logger {
        return this._logger
    }

    addLogger(logger: Logger) {
        this._logger = logger
    }

    public addCell(kind: 'code' | 'markdown', text: string) {
        if (this.notebook) {
            this.notebook.addCell(kind, text);
        }
    }

}
