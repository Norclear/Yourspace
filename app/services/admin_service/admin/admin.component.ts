import { AdminService } from './../admin.service';
import { AuthService } from './../../auth.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  title = "Admin"

  constructor(private auth: AuthService,public admin_s: AdminService) { }
  
  token;

  user;

  ngOnInit(): void {
    this.token = this.auth.get_token()
  }


}
