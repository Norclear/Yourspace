import { AuthService } from './../services/auth.service';
import { ErrorService } from 'src/app/services/error.service';
import { PostService } from '../services/post_service/post.service';
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-my-posts',
  templateUrl: 'my-posts.component.html',
  styleUrls: ['my-posts.component.scss']
})
export class MyPostsComponent implements OnInit {

  postResults = [];

  returnedResult = null;

  title = 'My Posts';

  constructor(private http: HttpClient, private post_s: PostService, private error_s: ErrorService, private auth: AuthService) { }

  ngOnInit(): void {

    this.auth.loggedIn.subscribe(data => {
      const loggedIn = data;
      if (loggedIn == false) {
        this.auth.user_not_authorised()
      }
    });

    const token = this.auth.get_token()



    this.post_s.my_posts(token).subscribe(response => {
      for (const value in response) {
        this.postResults.push(response[value])
      }

      if (this.postResults.length == 0) {
        this.returnedResult = false
        return
      }

      this.returnedResult = true
    },
      error => {
        this.error_s.handle_error(error)
    })
  }

}
