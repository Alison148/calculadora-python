import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  calcular(operacao: string, valor1: number, valor2?: number): Observable<any> {
    const params = new URLSearchParams();
    params.append('operacao', operacao);
    params.append('valor1', valor1.toString());
    if (valor2 !== undefined && valor2 !== null) {
      params.append('valor2', valor2.toString());
    }

    const url = `${this.baseUrl}/calcular?${params.toString()}`;
    return this.http.get<any>(url);
  }
}
