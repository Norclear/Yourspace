import { CommentService } from './../services/comment_service/comment.service';
import { AuthService } from './../services/auth.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PostService } from '../services/post_service/post.service';
import { ErrorService } from '../services/error.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit {

  token = null;

  receivedData;

  title = 'loading...';
  
  description;

  attachment;

  ownerUsername;

  postDate;

  post_id: Number;

  loggedIn;

  comments = null;

  user_data;

  constructor(private error_s: ErrorService, private route: ActivatedRoute, private post_s:PostService, private auth: AuthService, public comment_s: CommentService) { 
    
  }

  ngOnInit(): void {

     this.route.params.subscribe(params => {
      this.post_id = params['postId'];
       

    this.auth.loggedIn.subscribe(data => {
      this.loggedIn = data;
    });
    this.auth.userData.subscribe(data => {
      this.user_data = data;
    });
       
    

    this.token = this.auth.get_token()
    
    this.post_s.get_post(this.token, this.post_id).subscribe(postData => {
      this.title = postData['title']
      this.description = postData['description']
      this.ownerUsername = postData['ownerUsername']
      this.postDate = postData['postDate']
      if (postData['attachment'] !== null) {
      const img_data = postData['attachment']
      this.attachment = new Image();
      this.attachment.src = `data:image/${img_data.extension};base64,${img_data.base64}`;
      }
      this.comment_s.get_comments(this.post_id).subscribe(response => {
        this.comments = response
        this.receivedData = true;
    },
      error => {
        this.error_s.handle_error(error)
    })
      
    },
      error => {
        this.error_s.handle_error(error)
      }
    );
    });
    

  
    
  }

}

