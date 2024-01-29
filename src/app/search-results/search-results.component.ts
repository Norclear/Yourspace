import { environment } from 'src/environments/environment';
import { ErrorService } from './../services/error.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})
export class SearchResultsComponent implements OnInit {

  url = environment.baseUrl

  returnedResult = null;

  userResults = [];
  postResults = [];

  totalUserResults: number;
  totalPostResults: number;

  userResultsToShow = 3;
  postResultsToShow = 3;

  
  query: string

  constructor(private route: ActivatedRoute, private http: HttpClient, private error_s: ErrorService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.returnedResult = null
      this.query = params['query'].trim() || false;
        this.userResults = [];
        this.postResults = []; 
      this.totalUserResults = 0;
      this.totalPostResults = 0;
      this.userResultsToShow = 3;
      this.postResultsToShow = 3;
      this.http.get(`${this.url}/filter?query=${this.query}`).subscribe(response => {
        for (const value in response['users']) {
          this.userResults.push(response['users'][value])
        }
        for (const value in response['posts']) {
          this.postResults.push(response['posts'][value])
        }
        this.totalUserResults = this.userResults.length
        this.totalPostResults = this.postResults.length
        this.returnedResult = true
      },
        error => {
        this.error_s.handle_error(error)
      })
    });
  }
  
   getSafeUrl(picture) {
     return 'data:image/svg+xml,' + encodeURIComponent(picture);
   }
  
  showMoreUsers() {
    this.userResultsToShow += 3;
  }
  showMorePosts() {
    this.postResultsToShow += 3;
  }
}
 