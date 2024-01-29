import { AuthService } from 'src/app/services/auth.service';
import { NotificationService } from '../notification_service/notification.service';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { ErrorService } from '../error.service';

@Injectable({
  providedIn: 'root'
})
export class CommentService {

  url = environment.baseUrl

  headers = environment.headers

  prefix = '/comments'

  currentUrl;

  constructor(private http: HttpClient, private error_s: ErrorService, private notification_s: NotificationService, private auth:AuthService) {}

  create_comment(postId, token, comment) {

    this.headers['token'] = token
    this.headers['postId'] = postId

    const body = {
      'comment': comment
    }

    this.http.post(`${this.url}${this.prefix}/create`, body, { headers: this.headers }).subscribe(response => {
      this.notification_s.notify('success')
      this.auth.reload()

    },
      error => {
        this.error_s.handle_error(error)
    })


  }

  delete_comment(token, id) {

    this.headers['token'] = token

    
    this.http.delete(`${this.url}${this.prefix}/delete/${id}`, { headers: this.headers }).subscribe(response => {
      this.notification_s.notify('deleted')
      this.auth.reload()
    },
      error => {
        this.error_s.handle_error(error)
    });
  }

  get_comments(id) {

   return this.http.get(`${this.url}${this.prefix}/get/${id}`, {headers: this.headers})

  }

}
