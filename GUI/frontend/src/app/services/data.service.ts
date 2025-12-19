import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getDoppler(frameIndex: number = 0): Observable<any> {
    // Richiedi un solo frame per simulazione live
    return this.http.get(`${this.apiUrl}/doppler?frame_index=${frameIndex}`);
  }

  getAngle(frameIndex: number = 0): Observable<any> {
    // Richiedi un solo frame per simulazione live
    return this.http.get(`${this.apiUrl}/angle?frame_index=${frameIndex}`);
  }

  getTargets(frameIndex: number = 0): Observable<any> {
    // Richiedi la prediction per uno specifico frame
    return this.http.get(`${this.apiUrl}/targets?frame_index=${frameIndex}`);
  }

  getChartData(): Observable<any> {
    console.log('Making HTTP request to:', `${this.apiUrl}/chart-data`);
    return this.http.get(`${this.apiUrl}/chart-data`);
  }
}
