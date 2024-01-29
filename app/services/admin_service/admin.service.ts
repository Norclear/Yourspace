import { response } from 'express';
import { environment } from './../../../environments/environment.prod';
import { NotificationService } from './../notification_service/notification.service';
import { ErrorService } from './../error.service';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  url = environment.baseUrl

  headers = environment.headers

  prefix = '/admin'

  constructor(private http:HttpClient,private error_s: ErrorService, private notification_s: NotificationService) { }

  delete_user(token, user) {

  this.headers['token'] = token

    this.http.delete(`${this.url}${this.prefix}/delete_user/${user}`, { headers: this.headers}).subscribe(response => {
      this.notification_s.notify('deleted')
    },
      error => {
        this.error_s.handle_error(error)
    })
  }

}
