import { NotificationService } from './../notification.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss']
})
export class ToastComponent implements OnInit {

  timeout = (this.notificationService.notifcationTime) / 2
  
  classes;

  data = {
    'success': {
      'message': 'Success',
      'src':'../../../../assets/created_resource.svg'
    },
    'deleted': {
      'message': 'Deleted',
      'src':'../../../../assets/deleted_resource.svg'
    }
  }

  notifications = [];

  constructor(private notificationService: NotificationService) { }
  
ngOnInit() {
  this.notificationService.notifications.subscribe(notifications => {
    this.notifications = notifications;
    this.notifications.forEach(notification => {
      this.classes = notification.type + ' slide-in-blurred-bottom'
      const div = document.getElementById(notification.id)
      setTimeout(() => {
        this.classes = notification.type + ' slide-in-blurred-top'
      }, this.timeout);
    });
  });
}

  
}
