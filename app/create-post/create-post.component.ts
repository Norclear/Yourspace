import { PostService } from '../services/post_service/post.service';
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { AuthService } from '../services/auth.service';


@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit {

  @ViewChild('inputFile') inputFile: ElementRef;
  
  isLoaded = false;

  token;

  description: string = null;
  
  privatePost: boolean = false;
  
  selectedFile: File = null;

  selectedFileUrl: any;

  title = 'Create Post'


  constructor(private sanitizer: DomSanitizer, private auth: AuthService, public post_s: PostService) { }

  ngOnInit(): void {
    this.auth.loggedIn.subscribe(data => {
      const loggedIn = data;
      if (loggedIn == false) {
        this.auth.user_not_authorised()
      }
    });

    this.token = this.auth.get_token()
      
  }

  uploadImage(event) {

    const maxSize = 2000000
  
    this.selectedFile = event.target.files[0];

    if (this.selectedFile.size > maxSize) {
      document.getElementById('error-text').textContent = "Image can't be larger than 2MB"
      this.removeImage()
      return
    }

    this.isLoaded = true
    this.selectedFileUrl = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(this.selectedFile))
  }

  removeImage() {
    this.selectedFile = null
    this.isLoaded = false
    this.inputFile.nativeElement.value = ''
  }

}
