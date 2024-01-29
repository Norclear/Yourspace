import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
  
export class NavbarComponent implements OnInit {

  loggedIn: boolean;


  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    this.auth.loggedIn.subscribe(data => {
      this.loggedIn = data;
    });
  }

} 
