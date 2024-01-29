import { ErrorService } from 'src/app/services/error.service';
import { response } from 'express';
import { UserService } from './../services/user.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
  
export class UserComponent implements OnInit {

  receivedData = null

  url: string = "http://localhost:8000";

  username: string
  reg_date: string
  permissions: string
  
  constructor(private route: ActivatedRoute, private user_s: UserService, private error_s: ErrorService ) {

    this.route.params.subscribe(params => {
      this.username = params['username'];
      this.receivedData = false
      this.user_s.get_user(this.username).subscribe(response => {
        this.reg_date = response[0]
        this.permissions = response[1]
        this.receivedData = true
      },
        error => {
          this.error_s.handle_error(error)
      })
    });
    
  }

  ngOnInit() {
  }

}




