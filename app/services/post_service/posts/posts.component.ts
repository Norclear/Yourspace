import { ErrorService } from './../../error.service';
import { PostService } from './../post.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-posts',
  templateUrl: './posts.component.html',
  styleUrls: ['./posts.component.scss']
})
export class PostsComponent implements OnInit {

  returnedResult = null;

  postResults;

  title = 'Feed';

  constructor(private post_s: PostService, private error_s: ErrorService) { }

  ngOnInit(): void {
    this.post_s.feed().subscribe(response => {
      this.postResults = response;
      this.returnedResult = true
    },
      error => {
        this.error_s.handle_error(error)
    })
  }

}
