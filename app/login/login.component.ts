import { UserService } from './../services/user.service';
import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  title = 'Login';
  
  constructor(public user_s: UserService, private auth: AuthService) { }

  ngOnInit(): void {
      this.auth.loggedIn.subscribe(data => {
        const loggedIn = data;
        if (loggedIn) {
          this.auth.user_authorised()
        }
      });
    }
  
}
