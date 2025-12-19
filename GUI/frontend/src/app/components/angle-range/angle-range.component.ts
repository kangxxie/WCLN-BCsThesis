
import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-angle-range',
  templateUrl: './angle-range.component.html',
  styleUrls: ['./angle-range.component.css']
})
export class AngleRangeComponent implements OnInit, OnDestroy {
  plotData: any[] = [];
  plotLayout: any = {};
  currentFrameIndex: number = 0;
  totalFrames: number = 0;
  animationInterval: any = null;
  animationSpeed: number = 1000;

  heatmapCells: Array<{row: number, col: number, value: number, color: string}> = [];
  rows: number = 0;
  cols: number = 0;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.currentFrameIndex = 0;
    this.fetchAndAnimate();
    // Aggiorna costantemente la visualizzazione Angle
    this.animationInterval = setInterval(() => {
      this.currentFrameIndex = (this.currentFrameIndex + 1) % (this.totalFrames || 1);
      this.fetchAngleFrame(this.currentFrameIndex);
    }, this.animationSpeed);
  }

  ngOnDestroy(): void {
    if (this.animationInterval) {
      clearInterval(this.animationInterval);
    }
  }

  fetchAngleFrame(frameIndex: number, callback?: () => void): void {
    console.log('[FRONTEND] Richiesta frame Angle:', frameIndex);
    this.dataService.getAngle(frameIndex).subscribe({
      next: (data: any) => {
        console.log('[FRONTEND] Ricevuto frame Angle:', frameIndex, 'Data:', data);
        if (data && data["Angle-Range Map"]) {
          this.totalFrames = data["available_frames"] || 1;
          const map = data["Angle-Range Map"];
          this.rows = map.length;
          this.cols = map[0]?.length || 0;
          // Flatten and colorize
          const flat: Array<{row: number, col: number, value: number, color: string}> = [];
          let min = Infinity, max = -Infinity;
          for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
              const v = map[r][c];
              if (v < min) min = v;
              if (v > max) max = v;
            }
          }
          function viridisColor(val: number, min: number, max: number): string {
            const t = (val - min) / (max - min || 1);
            const stops = [
              [68, 1, 84], [71, 44, 122], [59, 81, 139], [44, 113, 142],
              [33, 144, 141], [39, 173, 129], [92, 200, 99], [170, 220, 50], [253, 231, 37]
            ];
            const idx = Math.floor(t * (stops.length - 1));
            const [r, g, b] = stops[idx];
            return `rgb(${r},${g},${b})`;
          }
          for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
              flat.push({
                row: r,
                col: c,
                value: map[r][c],
                color: viridisColor(map[r][c], min, max)
              });
            }
          }
          this.heatmapCells = flat;
          console.log('[FRONTEND] Aggiornata heatmapCells, frame:', frameIndex, 'cells:', flat.length);
          if (callback) callback();
        } else {
          this.heatmapCells = [];
          console.warn('[FRONTEND] Nessun dato Angle-Range Map per frame:', frameIndex);
        }
      },
      error: (error) => {
        console.error('[FRONTEND] Errore fetch Angle-Range frame:', frameIndex, error);
        this.heatmapCells = [];
        if (callback) callback();
      }
    });
  }

  fetchAndAnimate(): void {
    if (this.animationInterval) {
      clearInterval(this.animationInterval);
    }
    this.fetchAngleFrame(this.currentFrameIndex, () => {
      if (this.totalFrames > 1) {
        this.animationInterval = setInterval(() => {
          if (this.currentFrameIndex < this.totalFrames - 1) {
            this.currentFrameIndex++;
          } else {
            this.currentFrameIndex = 0;
          }
          this.fetchAngleFrame(this.currentFrameIndex);
        }, 10);
      }
    });
  }
}
