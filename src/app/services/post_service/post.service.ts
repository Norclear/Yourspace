import { NotificationService } from '../notification_service/notification.service';
import { ErrorService } from 'src/app/services/error.service';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class PostService {

  url = environment.baseUrl

  headers = environment.headers

  prefix = '/posts'

  constructor(private http: HttpClient, private router: Router, private error_s: ErrorService, private notifcation_s: NotificationService) { }

  create_post(token, title, description, attachment, privatePost) {

    this.headers['token'] = token

    let body = {
      'title': title,
      'description': description,
      'private': privatePost
    }

    if (attachment) {
      let reader = new FileReader();
      reader.readAsDataURL(attachment);
      reader.onload = () => {
        attachment = reader.result;
        body['attachment'] = attachment;
        this.http.post(`${this.url}${this.prefix}/create_post`, body, { headers: this.headers }).subscribe((response) => {
          this.notifcation_s.notify('success')
          this.router.navigate(['/home'])
        },
          error => {
            this.error_s.handle_error(error)
          })
      }
    }
    else {
      this.http.post(`${this.url}${this.prefix}/create_post`, body, { headers: this.headers }).subscribe((response) => {
        this.notifcation_s.notify('success')
            this.router.navigate(['/home'])
      },
        error => {
          this.error_s.handle_error(error)
        })
    }

  }
  
  get_post(token, postId) {

    this.headers['token'] = token
    
    return this.http.get(`${this.url}${this.prefix}/get_post/${postId}`, { headers: this.headers });
  }

  edit_post(token, id, title, description) {

    this.headers['token'] = token
    
    const body = {
      'title': title,
      'description': description,
    }
    
    this.http.put(`${this.url}${this.prefix}/edit/${id}`, body, { headers: this.headers }).subscribe(response => {
      this.notifcation_s.notify('success')
      this.router.navigate(['/home'])
    },
      error => {
        this.error_s.handle_error(error)
      })
  }

  delete_post(token, id) {

    this.headers['token'] = token

    this.http.delete(`${this.url}${this.prefix}/delete/${id}`, { headers: this.headers }).subscribe(response => {
      this.router.navigate(['/home'])
      this.notifcation_s.notify('deleted')
    },
      error => {
        this.error_s.handle_error(error)
      })
  }

  my_posts(token) {

  this.headers['token'] = token

    return this.http.get(`${this.url}${this.prefix}/my_posts`, { headers: this.headers })

  }

  feed() {
    
    return this.http.get(`${this.url}${this.prefix}/feed`, {headers:this.headers})
    
  }
}

