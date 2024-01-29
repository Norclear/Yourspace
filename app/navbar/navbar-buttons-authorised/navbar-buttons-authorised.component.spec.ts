import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavbarButtonsAuthorisedComponent } from './navbar-buttons-authorised.component';

describe('NavbarButtonsAuthorisedComponent', () => {
  let component: NavbarButtonsAuthorisedComponent;
  let fixture: ComponentFixture<NavbarButtonsAuthorisedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NavbarButtonsAuthorisedComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NavbarButtonsAuthorisedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
