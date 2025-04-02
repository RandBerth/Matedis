// Base de conocimientos del chatbot (hechos y reglas)
const knowledgeBase = {
  // Hechos sobre cursos
  cursos: {
    'Ingeniería de Software': {
      requisito: 'Programación I',
      creditos: 4,
      horario: 'Lunes y Miércoles 10:00-12:00'
    },
    'Programación I': {
      requisito: null,
      creditos: 3,
      horario: 'Martes y Jueves 14:00-16:00'
    },
    'Bases de Datos': {
      requisito: 'Programación I',
      creditos: 4,
      horario: 'Viernes 8:00-12:00'
    },
    'Inteligencia Artificial': {
      requisito: 'Matemáticas Discretas AND Programación I',
      creditos: 5,
      horario: 'Lunes 16:00-19:00'
    }
  },
  
  // Reglas lógicas para inferencias
  reglas: {
    'puedeTomar': (curso, cursosAprobados) => {
      const requisitos = knowledgeBase.cursos[curso].requisito;
      
      if (!requisitos) return true; // No tiene requisitos
      
      // Procesar expresiones lógicas con AND y OR
      const partes = requisitos.split(/(AND|OR)/).map(s => s.trim());
      
      let resultado;
      let operador = null;
      
      for (const parte of partes) {
        if (parte === 'AND' || parte === 'OR') {
          operador = parte;
        } else {
          const valor = cursosAprobados.includes(parte);
          
          if (resultado === undefined) {
            resultado = valor;
          } else if (operador === 'AND') {
            resultado = resultado && valor;
          } else if (operador === 'OR') {
            resultado = resultado || valor;
          }
        }
      }
      
      return resultado;
    }
  }
};

// Motor de inferencia lógica
class Chatbot {
  constructor() {
    this.cursosAprobados = [];
    this.historial = [];
  }
  
  // Método para evaluar expresiones lógicas
  evaluarExpresion(expresion) {
    const partes = expresion.split(/(AND|OR|NOT)/).map(s => s.trim()).filter(s => s);
    
    let resultado;
    let operador = null;
    
    for (const parte of partes) {
      if (parte === 'AND' || parte === 'OR' || parte === 'NOT') {
        operador = parte;
      } else {
        let valor;
        
        // Verificar si es un hecho directo
        if (knowledgeBase.cursos[parte]) {
          valor = true;
        } else if (this.cursosAprobados.includes(parte)) {
          valor = true;
        } else {
          valor = false;
        }
        
        // Aplicar NOT si es necesario
        if (operador === 'NOT') {
          valor = !valor;
          operador = null;
        }
        
        if (resultado === undefined) {
          resultado = valor;
        } else if (operador === 'AND') {
          resultado = resultado && valor;
        } else if (operador === 'OR') {
          resultado = resultado || valor;
        }
      }
    }
    
    return resultado;
  }
  
  // Método principal para procesar preguntas
  procesarPregunta(pregunta) {
    this.historial.push(`Usuario: ${pregunta}`);
    
    // Convertir a minúsculas y eliminar signos de interrogación
    const preguntaNormalizada = pregunta.toLowerCase().replace('?', '').trim();
    const palabras = preguntaNormalizada.split(' ');
    
    // Patrones de preguntas
    if (preguntaNormalizada.includes('puedo tomar') || preguntaNormalizada.includes('puede tomar')) {
      const curso = Object.keys(knowledgeBase.cursos).find(c => preguntaNormalizada.includes(c.toLowerCase()));
      
      if (!curso) {
        const respuesta = "No reconozco ese curso. ¿Podrías ser más específico?";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
      
      const puedeTomar = knowledgeBase.reglas.puedeTomar(curso, this.cursosAprobados);
      const respuesta = puedeTomar 
        ? `Sí, puedes tomar ${curso}. Requisitos cumplidos.` 
        : `No puedes tomar ${curso}. Faltan requisitos: ${knowledgeBase.cursos[curso].requisito || 'ninguno'}`;
      
      this.historial.push(`Chatbot: ${respuesta}`);
      return respuesta;
    }
    else if (preguntaNormalizada.includes('horario de')) {
      const curso = Object.keys(knowledgeBase.cursos).find(c => preguntaNormalizada.includes(c.toLowerCase()));
      
      if (!curso) {
        const respuesta = "No reconozco ese curso. ¿Podrías ser más específico?";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
      
      const respuesta = `El horario de ${curso} es: ${knowledgeBase.cursos[curso].horario}`;
      this.historial.push(`Chatbot: ${respuesta}`);
      return respuesta;
    }
    else if (preguntaNormalizada.includes('créditos de')) {
      const curso = Object.keys(knowledgeBase.cursos).find(c => preguntaNormalizada.includes(c.toLowerCase()));
      
      if (!curso) {
        const respuesta = "No reconozco ese curso. ¿Podrías ser más específico?";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
      
      const respuesta = `El curso ${curso} vale ${knowledgeBase.cursos[curso].creditos} créditos.`;
      this.historial.push(`Chatbot: ${respuesta}`);
      return respuesta;
    }
    else if (preguntaNormalizada.includes('aprobé') || preguntaNormalizada.includes('aprobado')) {
      const curso = Object.keys(knowledgeBase.cursos).find(c => preguntaNormalizada.includes(c.toLowerCase()));
      
      if (!curso) {
        const respuesta = "No reconozco ese curso. ¿Podrías ser más específico?";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
      
      if (!this.cursosAprobados.includes(curso)) {
        this.cursosAprobados.push(curso);
        const respuesta = `He registrado que aprobaste ${curso}.`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      } else {
        const respuesta = `Ya tenías registrado que aprobaste ${curso}.`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
    }
    else if (preguntaNormalizada.includes('evalúa') || preguntaNormalizada.includes('verifica')) {
      // Extraer la expresión lógica (ejemplo: "evalúa Programación I AND Matemáticas Discretas")
      const expresion = preguntaNormalizada.replace('evalúa', '').replace('verifica', '').trim();
      
      try {
        const resultado = this.evaluarExpresion(expresion);
        const respuesta = `La expresión "${expresion}" es ${resultado ? 'verdadera' : 'falsa'}.`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      } catch (e) {
        const respuesta = "No pude evaluar esa expresión. Asegúrate de usar AND, OR, NOT correctamente.";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
    }
    else if (preguntaNormalizada.includes('qué necesito para tomar') || preguntaNormalizada.includes('requisitos para')) {
      const curso = Object.keys(knowledgeBase.cursos).find(c => preguntaNormalizada.includes(c.toLowerCase()));
      if (!curso) {
        const respuesta = "No reconozco ese curso. ¿ Podrias ser mas especifico?";
        this.historial.push(`Chatbot ${respuesta}`);
        return respuesta;
      }

      const requisitos = knowledgeBase.cursos[curso].requisito;
      const respuesta = requisitos ? `Para tomar ${curso}, necesitas: ${requisitos}.` : `No hay requisitos para el curso ${curso}`;

      this.historial.push(`Chatbot ${respuesta}`);
      return respuesta;
    }
    else if (preguntaNormalizada.includes('qué necesito para tomar') || preguntaNormalizada.includes('requisitos para')) {
      const curso = Object.keys(knowledgeBase.cursos).find(c => preguntaNormalizada.includes(c.toLowerCase()));
      
      if (!curso) {
        const respuesta = "No reconozco ese curso. ¿Podrías ser más específico?";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
    
      const requisitos = knowledgeBase.cursos[curso].requisito;
      const respuesta = requisitos ? `Para tomar ${curso}, necesitas: ${requisitos}.` : `No hay requisitos para tomar ${curso}.`;
      
      this.historial.push(`Chatbot: ${respuesta}`);
      return respuesta;
    }
    else {
      const respuesta = "No entendí tu pregunta. Puedo ayudarte con:\n- Horarios de cursos\n- Créditos de cursos\n- Requisitos para tomar cursos\n- Evaluar expresiones lógicas (AND, OR, NOT)";
      this.historial.push(`Chatbot: ${respuesta}`);
      return respuesta;
    }
  }
  
  // Mostrar historial de conversación
  mostrarHistorial() {
    return this.historial.join('\n');
  }
}

// Ejemplo de uso
const bot = new Chatbot();

// Pruebas de interacción
console.log(bot.procesarPregunta("¿Puedo tomar Ingeniería de Software?"));
console.log(bot.procesarPregunta("Aprobé Programación I"));
console.log(bot.procesarPregunta("¿Puedo tomar Ingeniería de Software?"));
console.log(bot.procesarPregunta("¿Cuál es el horario de Bases de Datos?"));
console.log(bot.procesarPregunta("Evalúa Programación I AND Bases de Datos"));
console.log(bot.procesarPregunta("Evalúa Programación I OR Matemáticas Discretas"));
console.log(bot.procesarPregunta("Evalúa NOT Programación I"));

console.log("\nHistorial completo:");
console.log(bot.mostrarHistorial());