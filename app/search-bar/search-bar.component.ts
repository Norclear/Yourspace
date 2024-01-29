import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {

  constructor(private router:Router) { }

  ngOnInit(): void {
  }

  search(input) {
  
    if (!input) {
      return
    }

   this.router.navigate(
      ['/search'], 
      { queryParams: { query: input } }
    ); 
  }
}
