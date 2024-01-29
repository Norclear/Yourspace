import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  private notificationsSubject = new BehaviorSubject<any[]>([]);
  notifications = this.notificationsSubject.asObservable();

  notifcationTime = 2000 // keep in mind that the animation class of the toast componenet will change after {notifcationTime}ms/2

  constructor() { }

  notify(type) {
    const id = new Date().getTime();
    let state = 1 
    const notification = { id, type, state };
    this.notificationsSubject.next([...this.notificationsSubject.value, notification]);
    setTimeout(() => {
      notification.state = state;
      this.notificationsSubject.next(this.notificationsSubject.value.filter(n => {
        n.id !== id
      }));
    }, this.notifcationTime);
     

  }
    
}

