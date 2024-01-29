import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-unauthorised-access',
  templateUrl: './unauthorised-access.component.html',
  styleUrls: ['./unauthorised-access.component.scss']
})
export class UnauthorisedAccessComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
    
  goBack() {
      window.history.back();
  }
}
