import { Component } from '@angular/core';

import { BackendApi } from '../../services/backend-api';

@Component({
  selector: 'app-settings',
  imports: [],
  templateUrl: './settings.html',
  styleUrl: './settings.css',
})
export class Settings {
  readonly frontendUrl = 'http://localhost:18072';
  readonly spaghettiChefUrl = 'http://localhost:18080';

  constructor(readonly backendApi: BackendApi) {}
}
