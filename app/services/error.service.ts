import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class ErrorService {

  error;

  constructor(private router: Router) { }

  server_error(error_str) {
    this.error = error_str;

    if (this.error == null || this.error == '' || this.error == 0) {
      this.error == "an error of unknown proportions"
    }

    this.router.navigate(['/internalServerError'])
  }

  forbidden() {
    this.router.navigate(['/forbidden'])
  }

  not_found() {
    this.router.navigate(['/notfound'])
  }

  unathorised() {
    this.router.navigate(['/unathorised'])
  }

  bad_request(error_str) {
    document.getElementById('error-text').textContent = error_str
  }

  handle_error(error: HttpErrorResponse) {
    switch (error.status) {
      case 400:
        this.bad_request(error.error.detail)
        break
      case 401:
        this.unathorised()
        break
      case 403:
        this.forbidden()
        break
      case 404:
        this.not_found()
        break
      case 500:
        this.server_error(error.error.detail)
   }
  }
}

//  if (error.status == 400) {
//       this.bad_request(error.error.detail)
//     }
//     else if (error.status == 401) {
//       this.unathorised()
//     }
//     else if (error.status == 403) {
//       this.forbidden()
//     }
//     else if (error.status == 404) {
//       this.not_found()
//     }
//     else if (error.status == 500) {
//       this.server_error(error)
//     }