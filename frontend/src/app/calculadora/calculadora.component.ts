import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-calculadora',
  templateUrl: './calculadora.component.html',
  styleUrls: ['./calculadora.component.css']
})
export class CalculadoraComponent {
  operacao = '+';
  valor1: number = 0;
  valor2: number = 0;
  resultado: number | null = null;
  expressao: string = '';

  constructor(private api: ApiService) {}

  precisaSegundoValor() {
    return !['sin', 'cos', 'tan', 'sqrt', 'log'].includes(this.operacao);
  }

  calcular() {
    this.api.calcular(this.operacao, this.valor1, this.valor2).subscribe({
      next: (res) => {
        this.resultado = res.resultado;
        this.expressao = this.montarExpressao();
      },
      error: (err) => {
        console.error('Erro ao calcular:', err);
        this.resultado = null;
      }
    });
  }

  montarExpressao(): string {
    if (this.precisaSegundoValor()) {
      return `${this.valor1} ${this.operacao} ${this.valor2}`;
    } else {
      return `${this.operacao}(${this.valor1})`;
    }
  }
}
