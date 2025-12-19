import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../../services/data.service';
import { Subscription, interval } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-visualization',
  templateUrl: './visualization.component.html',
  styleUrls: ['./visualization.component.css']
})
export class VisualizationComponent implements OnInit, OnDestroy {
  private dataSubscription?: Subscription;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    // TODO: implement data fetching and visualization
    this.dataSubscription = interval(5000).pipe(
      switchMap(() => this.dataService.getDoppler())
    ).subscribe({
      next: (data) => {
        console.log('Doppler data:', data);
        // TODO: Update visualization with new data
      },
      error: (error) => {
        console.error('Error fetching Doppler data:', error);
      }
    });
  }

  ngOnDestroy(): void {
    if (this.dataSubscription) {
      this.dataSubscription.unsubscribe();
    }
  }
}
