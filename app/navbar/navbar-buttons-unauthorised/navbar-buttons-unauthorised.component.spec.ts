import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavbarButtonsUnauthorisedComponent } from './navbar-buttons-unauthorised.component';

describe('NavbarButtonsUnauthorisedComponent', () => {
  let component: NavbarButtonsUnauthorisedComponent;
  let fixture: ComponentFixture<NavbarButtonsUnauthorisedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NavbarButtonsUnauthorisedComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavbarButtonsUnauthorisedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
