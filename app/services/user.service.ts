import { AuthService } from 'src/app/services/auth.service';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ErrorService } from './error.service';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {


  url = environment.baseUrl

  headers = environment.headers

  prefix = '/users'

  constructor(private http: HttpClient, private auth: AuthService, private error_s: ErrorService) { }

  create_user(username, password) {
    

    const body = {
      'username': username,
      'password': password
    }

    this.http.post(`${this.url}${this.prefix}/create_user`, body, {headers:this.headers}).subscribe((response) => {
      this.login(username, password)
    },
      error => {
        this.error_s.handle_error(error)
      })
  }

  login(username, password) {
  
    const body = {
      'username': username,
      'password': password
    }

    this.http.post(`${this.url}/login`, body,{headers:this.headers}).subscribe((response) => {
      this.auth.set_token(response['token'])
      this.auth.user_authorised()
    },
      error => {
        this.error_s.handle_error(error)
      })
  }

  get_user(username) {
    return this.http.get(`${this.url}${this.prefix}/user/${username}`, {headers:this.headers})
  }
}