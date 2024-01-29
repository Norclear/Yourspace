import { UserService } from './../services/user.service';
import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';



@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
  
export class SignupComponent implements OnInit {

  title = 'Sign Up';

  constructor(public user_s: UserService, private auth: AuthService) { };

  loggedIn: boolean;

  ngOnInit(): void {
      this.auth.loggedIn.subscribe(data => {
        this.loggedIn = data;
        if (this.loggedIn) {
          this.auth.user_authorised()
        }
      });
    }

};
