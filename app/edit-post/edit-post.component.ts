import { ErrorService } from 'src/app/services/error.service';
import { Component, OnInit } from '@angular/core';
import { PostService } from '../services/post_service/post.service';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-edit-post',
  templateUrl: './edit-post.component.html',
  styleUrls: ['./edit-post.component.scss']
})
  
export class EditPostComponent implements OnInit {

  post_id;

  title;

  description;

  receviedData = null;

  token;

  constructor(public post_s: PostService, private route: ActivatedRoute, private auth: AuthService, private error_s: ErrorService) { }

  ngOnInit(): void {

    this.auth.loggedIn.subscribe(data => {
        const loggedIn = data;
        if (loggedIn == false) {
          this.auth.user_not_authorised()
        }
    });

    this.token = this.auth.get_token()
    
    this.route.params.subscribe(params => {
      this.post_id = params['postId'];
      this.post_s.get_post(this.token, this.post_id).subscribe(postData => {
        this.title = postData['title']
        this.description = postData['description']
        this.receviedData = true
      })
    });
  }

}
