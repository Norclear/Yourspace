import { AdminService } from './services/admin_service/admin.service';
import { CommentService } from './services/comment_service/comment.service';
import { NotificationService } from './services/notification_service/notification.service';
import { UserService } from './services/user.service';
import { ErrorService } from './services/error.service';
import { PostService } from './services/post_service/post.service';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { LocationStrategy, PathLocationStrategy } from '@angular/common';

// MDB Modules
import { MdbAccordionModule } from 'mdb-angular-ui-kit/accordion';
import { MdbCarouselModule } from 'mdb-angular-ui-kit/carousel';
import { MdbCheckboxModule } from 'mdb-angular-ui-kit/checkbox';
import { MdbCollapseModule } from 'mdb-angular-ui-kit/collapse';
import { MdbDropdownModule } from 'mdb-angular-ui-kit/dropdown';
import { MdbFormsModule } from 'mdb-angular-ui-kit/forms';
import { MdbModalModule } from 'mdb-angular-ui-kit/modal';
import { MdbPopoverModule } from 'mdb-angular-ui-kit/popover';
import { MdbRadioModule } from 'mdb-angular-ui-kit/radio';
import { MdbRangeModule } from 'mdb-angular-ui-kit/range';
import { MdbRippleModule } from 'mdb-angular-ui-kit/ripple';
import { MdbScrollspyModule } from 'mdb-angular-ui-kit/scrollspy';
import { MdbTabsModule } from 'mdb-angular-ui-kit/tabs';
import { MdbTooltipModule } from 'mdb-angular-ui-kit/tooltip';
import { MdbValidationModule } from 'mdb-angular-ui-kit/validation';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from './header/header.component';
import { SignupComponent } from './signup/signup.component';
import {  RouterModule,Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { FormsModule } from '@angular/forms';
import { HomeComponent } from './home/home.component';
import { AuthService } from './services/auth.service';
import { UserComponent } from './user/user.component';
import { SearchBarComponent } from './search-bar/search-bar.component';
import { PageNotFoundComponent } from './response-pages/page-not-found/page-not-found.component';
import { SearchResultsComponent } from './search-results/search-results.component';
import { NavbarButtonsUnauthorisedComponent } from './navbar/navbar-buttons-unauthorised/navbar-buttons-unauthorised.component';
import { NavbarButtonsAuthorisedComponent } from './navbar/navbar-buttons-authorised/navbar-buttons-authorised.component';
import { CreatePostComponent } from './create-post/create-post.component';
import { LoaderComponent } from './loader/loader.component';
import { PostComponent } from './post/post.component';
import { PageForbiddenComponent } from './response-pages/page-forbidden/page-forbidden.component';
import { MyPostsComponent } from './my-posts/my-posts.component';
import { ManagePostComponent } from './services/post_service/manage-post/manage-post.component';
import { EditPostComponent } from './edit-post/edit-post.component';
import { ServerErrorComponent } from './response-pages/server-error/server-error.component';
import { UnauthorisedAccessComponent } from './response-pages/unauthorised-access/unauthorised-access.component';
import { SnackbarComponent } from './services/notification_service/snackbar/snackbar.component';
import { ToastComponent } from './services/notification_service/toast/toast.component';
import { CommentComponent } from './services/comment_service/comment/comment.component';
import { ManageCommentComponent } from './services/comment_service/manage-comment/manage-comment.component';
import { PostsComponent } from './services/post_service/posts/posts.component';
import { AdminComponent } from './services/admin_service/admin/admin.component';

const appRoute: Routes = [
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent },
  { path: 'posts', component: PostsComponent },
  { path: 'home/posts', component: MyPostsComponent },
  { path: 'search', component: SearchResultsComponent },
  { path: 'post', component: CreatePostComponent },
  { path: 'post/:postId', component: PostComponent },
  { path: 'post/:postId/edit', component: EditPostComponent },
  { path: 'user/:username', component: UserComponent },
  { path: 'admin', component: AdminComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'forbidden', component: PageForbiddenComponent }, 
  { path: 'notfound', component: PageNotFoundComponent },
  { path: 'unathorised', component: UnauthorisedAccessComponent },
  { path: 'internalServerError', component: ServerErrorComponent },
  { path: '**', component: PageNotFoundComponent}
]

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    HeaderComponent,
    SignupComponent,
    LoginComponent,
    HomeComponent,
    UserComponent,
    SearchBarComponent,
    PageNotFoundComponent,
    SearchResultsComponent,
    NavbarButtonsUnauthorisedComponent,
    NavbarButtonsAuthorisedComponent,
    CreatePostComponent,
    LoaderComponent,
    PostComponent,
    PageForbiddenComponent,
    MyPostsComponent,
    ManagePostComponent,
    EditPostComponent,
    ServerErrorComponent,
    UnauthorisedAccessComponent,
    SnackbarComponent,
    ToastComponent,
    CommentComponent,
    ManageCommentComponent,
    PostsComponent,
    AdminComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    BrowserAnimationsModule,
    MdbAccordionModule,
    MdbCarouselModule,
    MdbCheckboxModule,
    MdbCollapseModule,
    MdbDropdownModule,
    MdbFormsModule,
    MdbModalModule,
    MdbPopoverModule,
    MdbRadioModule,
    MdbRangeModule,
    MdbRippleModule,
    MdbScrollspyModule,
    MdbTabsModule,
    MdbTooltipModule,
    MdbValidationModule,
    HttpClientModule,
    RouterModule.forRoot(appRoute, {
  onSameUrlNavigation: 'ignore'
    })
  ],
  providers: [[AuthService, PostService, ErrorService, UserService, NotificationService, CommentService, AdminService], { provide: LocationStrategy, useClass: PathLocationStrategy }],
  bootstrap: [AppComponent]
})
export class AppModule { }
