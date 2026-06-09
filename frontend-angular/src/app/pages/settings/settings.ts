import { Component } from '@angular/core';

import { BackendApi } from '../../services/backend-api';

@Component({
  selector: 'app-settings',
  imports: [],
  templateUrl: './settings.html',
  styleUrl: './settings.css',
})
export class Settings {
  constructor(readonly backendApi: BackendApi) {}
}
