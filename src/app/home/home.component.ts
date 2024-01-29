import { AuthService } from './../services/auth.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  loggedIn: boolean;

  userData;

  title = 'Home';


  constructor(private auth: AuthService) { }

  ngOnInit(): void {
      this.auth.loggedIn.subscribe(data => {
        this.loggedIn = data;
        if (this.loggedIn == false) {
          this.auth.user_not_authorised()
        }
      });
    this.auth.userData.subscribe(data => {
        this.userData = data;
      });
    }
}
