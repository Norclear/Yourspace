import { AuthService } from './../../auth.service';
import { Component, OnInit,Input } from '@angular/core';
import { CommentService } from '../comment.service';

@Component({
  selector: 'app-manage-comment',
  templateUrl: './manage-comment.component.html',
  styleUrls: ['./manage-comment.component.scss']
})
export class ManageCommentComponent implements OnInit {

  token;

  @Input() id;

  constructor(public comment_s: CommentService, private auth:AuthService) { }

  ngOnInit(): void {

    this.token = this.auth.get_token()

  }

}
