import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar-buttons-authorised',
  templateUrl: './navbar-buttons-authorised.component.html',
  styleUrls: ['./navbar-buttons-authorised.component.scss']
})
export class NavbarButtonsAuthorisedComponent implements OnInit {

  userData;

  pictureUrl: SafeUrl;
  
  constructor(private auth: AuthService,private sanitizer: DomSanitizer, private router: Router) { }

  ngOnInit(): void {
    this.auth.userData.subscribe(data => {
      this.userData = data;
      this.pictureUrl = this.sanitizer.bypassSecurityTrustUrl('data:image/svg+xml,' + encodeURIComponent(this.userData.picture));
      });
  }
  
  logOut() {
    if (localStorage.getItem('token')) {
          localStorage.removeItem('token')
    }
    this.auth.user_not_authorised()
  }

  navigate(url) {
    this.router.navigate([url])
  }
}
