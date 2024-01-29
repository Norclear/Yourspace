import { Component, OnInit, Input } from '@angular/core';
import { PostService } from '../post.service';

@Component({
  selector: 'app-manage-post',
  templateUrl: './manage-post.component.html',
  styleUrls: ['./manage-post.component.scss']
})
export class ManagePostComponent implements OnInit {

  @Input() post_id: Number;

  token;

  constructor(public post_s: PostService ) { }

  ngOnInit(): void {

    this.token = localStorage.getItem('token')

  }

}
