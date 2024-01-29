import { catchError, map } from 'rxjs/operators';
import { of } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, NavigationEnd } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HostListener } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
  
export class AuthService {

  url = environment.baseUrl

  headers = environment.headers

  userData = new BehaviorSubject<JSON>(null);

  loggedIn = new BehaviorSubject<boolean>(null);


  constructor(private http: HttpClient, private router: Router) { 
      this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.token_status()
      } 
    })
  }
  
  token_status() {

    let token = localStorage.getItem('token') || null

    if (token == null) {
      this.loggedIn.next(false);
      return
    }

    this.headers['token'] = token

    this.http.get(`${this.url}/verify_token`, { 'headers': this.headers, 'responseType': 'text' }).pipe(
      map(response => {
        const parsed_response = JSON.parse(response)
        this.loggedIn.next(parsed_response.loggedIn) 
        this.userData.next(parsed_response.userData) 
      }),
      catchError(error => {
        console.log(error)
        this.loggedIn.next(false);
        return of(false)
      })
    ).subscribe()
  }

  get_token() {
    if (localStorage.getItem('token')) {
      return localStorage.getItem('token')
    }
    return false
  }

  set_token(token) {
    localStorage.setItem('token', token)
  }

  user_not_authorised() {
    this.router.navigate(['/login'])
  }

  user_authorised() {
    this.router.navigate(['/home'])
  }

  reload() {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([this.router.url]);
  }

}



