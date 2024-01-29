import { AuthService } from 'src/app/services/auth.service';
import { Component, OnInit, Input  } from '@angular/core';

@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.scss']
})
export class CommentComponent implements OnInit {

  @Input() comment;
  @Input() username;
  @Input() date;
  @Input() user;
  @Input() id;

  options = false;

  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    if (this.user == this.username) {
      this.options = true;
    }
  }

}
