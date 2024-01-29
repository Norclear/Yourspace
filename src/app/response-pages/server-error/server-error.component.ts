import { Component, OnInit } from '@angular/core';
import { ErrorService } from 'src/app/services/error.service';

@Component({
  selector: 'app-server-error',
  templateUrl: './server-error.component.html',
  styleUrls: ['./server-error.component.scss']
})
export class ServerErrorComponent implements OnInit {

  error = this.error_s.error;

  constructor(private error_s: ErrorService) { }

  ngOnInit(): void {
  }

  goBack() {
      window.history.back();
  }

}
