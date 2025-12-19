import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';

import * as PlotlyJS from 'plotly.js-dist-min';
import { PlotlyModule } from 'angular-plotly.js';

/*  ←— v6 uses a static property rather than forRoot()  */
PlotlyModule.plotlyjs = PlotlyJS;
import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { HomeComponent } from './pages/home/home.component';
import { VisualizationComponent } from './pages/visualization/visualization.component';
import { StatisticsComponent } from './pages/statistics/statistics.component';
import { DopplerRangeComponent } from './components/doppler-range/doppler-range.component';
import { AngleRangeComponent } from './components/angle-range/angle-range.component';
import { TargetCounterComponent } from './components/target-counter/target-counter.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    HomeComponent,
    VisualizationComponent,
    StatisticsComponent,
    DopplerRangeComponent,
    AngleRangeComponent,
    TargetCounterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule,
    HttpClientModule,
    FormsModule,
    PlotlyModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
