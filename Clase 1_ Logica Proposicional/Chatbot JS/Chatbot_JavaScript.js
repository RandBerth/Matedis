// Base de conocimientos del chatbot (hechos y reglas)
const knowledgeBase = {
  cursos: {
    "Ingeniería de Software": {
      requisito: "Programación I",
      creditos: 4,
      horario: "Lunes y Miércoles 10:00-12:00",
    },
    "Programación I": {
      requisito: null,
      creditos: 3,
      horario: "Martes y Jueves 14:00-16:00",
    },
    "Bases de Datos": {
      requisito: "Programación I",
      creditos: 4,
      horario: "Viernes 8:00-12:00",
    },
    "Inteligencia Artificial": {
      requisito: "Matemáticas Discretas AND Programación I",
      creditos: 5,
      horario: "Lunes 16:00-19:00",
    },
    "Matemáticas Discretas": {
      requisito: null,
      creditos: 4,
      horario: "Martes 8:00-11:00 y Jueves 8:00-10:00",
    },
  },

  reglas: {
    puedeTomar: (curso, cursosAprobados) => {
      if (!knowledgeBase.cursos[curso]) return false;

      const requisitos = knowledgeBase.cursos[curso].requisito;
      if (!requisitos) return true;

      const partes = requisitos.split(/(AND|OR)/).map((s) => s.trim());

      let resultado;
      let operador = null;

      for (const parte of partes) {
        if (parte === "AND" || parte === "OR") {
          operador = parte;
        } else {
          const valor = cursosAprobados.includes(parte);

          if (resultado === undefined) {
            resultado = valor;
          } else if (operador === "AND") {
            resultado = resultado && valor;
          } else if (operador === "OR") {
            resultado = resultado || valor;
          }
        }
      }

      return resultado;
    },

    cursosDisponibles: (cursosAprobados) => {
      return Object.keys(knowledgeBase.cursos).filter((curso) => {
        return (
          knowledgeBase.reglas.puedeTomar(curso, cursosAprobados) &&
          !cursosAprobados.includes(curso)
        );
      });
    },

    buscarCursoPorNombre: (nombre) => {
      const nombreLower = nombre.toLowerCase();
      // Buscar coincidencia exacta primero
      const cursos = Object.keys(knowledgeBase.cursos);
      const exacto = cursos.find((c) => c.toLowerCase() === nombreLower);
      if (exacto) return exacto;

      // Buscar coincidencia parcial ignorando números
      const nombreSinNumeros = nombreLower.replace(/\d+/g, "").trim();
      return cursos.find(
        (c) =>
          c.toLowerCase().includes(nombreSinNumeros) ||
          nombreSinNumeros.includes(c.toLowerCase())
      );
    },
  },
};

class Chatbot {
  constructor() {
    this.cursosAprobados = [];
    this.historial = [];
  }

  evaluarExpresion(expresion) {
    // Manejar operador en español
    const exprNormalizada = expresion
      .replace(/ y /gi, " AND ")
      .replace(/ o /gi, " OR ")
      .replace(/ no /gi, " NOT ")
      .replace(/\?/g, "")
      .trim();

    const partes = exprNormalizada
      .split(/(AND|OR|NOT)/)
      .map((s) => s.trim())
      .filter((s) => s);

    let resultado;
    let operador = null;

    for (const parte of partes) {
      if (parte === "AND" || parte === "OR" || parte === "NOT") {
        operador = parte;
      } else {
        let valor =
          this.cursosAprobados.includes(parte) || !!knowledgeBase.cursos[parte];

        if (operador === "NOT") {
          valor = !valor;
          operador = null;
        }

        if (resultado === undefined) {
          resultado = valor;
        } else if (operador === "AND") {
          resultado = resultado && valor;
        } else if (operador === "OR") {
          resultado = resultado || valor;
        }
      }
    }

    return resultado ?? false;
  }

  procesarPregunta(pregunta) {
    this.historial.push(`Usuario: ${pregunta}`);

    try {
      // 1. Preguntas sobre requisitos de cursos
      if (
        /¿?Puedo tomar (.+)\??/i.test(pregunta) ||
        /¿?Qué necesito para tomar (.+)\??/i.test(pregunta) ||
        /¿?Cuáles son los requisitos para (.+)\??/i.test(pregunta)
      ) {
        const match = pregunta.match(/tomar (.+?)(\?|$)|para (.+?)(\?|$)/i);
        const cursoInput = match ? match[1] || match[3] : null;
        const curso = cursoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoInput)
          : null;

        if (!curso) {
          const respuesta =
            "No reconozco ese curso. Los cursos disponibles son: " +
            Object.keys(knowledgeBase.cursos).join(", ");
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }

        if (
          pregunta.toLowerCase().includes("qué necesito") ||
          pregunta.toLowerCase().includes("requisitos para")
        ) {
          const requisitos = knowledgeBase.cursos[curso].requisito;
          const respuesta = requisitos
            ? `Para tomar ${curso} necesitas: ${requisitos}`
            : `${curso} no tiene requisitos previos`;
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        } else {
          const puedeTomar = knowledgeBase.reglas.puedeTomar(
            curso,
            this.cursosAprobados
          );
          const respuesta = puedeTomar
            ? `Sí, puedes tomar ${curso}. Cumples con los requisitos.`
            : `No puedes tomar ${curso}. Requisitos faltantes: ${
                knowledgeBase.cursos[curso].requisito || "ninguno"
              }`;
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }
      }

      // 2. Registro de cursos aprobados
      else if (
        /Aprobé (.+)/i.test(pregunta) ||
        /He aprobado (.+)/i.test(pregunta) ||
        /Registra que pasé (.+)/i.test(pregunta) ||
        /Ya terminé (.+)/i.test(pregunta)
      ) {
        const match = pregunta.match(
          /Aprobé (.+)|He aprobado (.+)|Registra que pasé (.+)|Ya terminé (.+)/i
        );
        const cursoInput = match
          ? match[1] || match[2] || match[3] || match[4]
          : null;
        const curso = cursoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoInput)
          : null;

        if (!curso) {
          const respuesta =
            "No reconozco ese curso. Por favor especifica un curso válido.";
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

      // 3. Consulta de información académica
      else if (
        /¿?Cuál es el horario de (.+)\??/i.test(pregunta) ||
        /¿?Qué días se imparte (.+)\??/i.test(pregunta) ||
        /¿?A qué hora es (.+)\??/i.test(pregunta)
      ) {
        const match = pregunta.match(
          /horario de (.+)|días se imparte (.+)|hora es (.+)/i
        );
        const cursoInput = match ? match[1] || match[2] || match[3] : null;
        const curso = cursoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoInput)
          : null;

        if (!curso) {
          const respuesta =
            "No reconozco ese curso. Por favor especifica un curso válido.";
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }

        const respuesta = `El horario de ${curso} es: ${knowledgeBase.cursos[curso].horario}`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      } else if (/¿?Cuántos créditos vale (.+)\??/i.test(pregunta)) {
        const match = pregunta.match(/créditos vale (.+)/i);
        const cursoInput = match ? match[1] : null;
        const curso = cursoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoInput)
          : null;

        if (!curso) {
          const respuesta =
            "No reconozco ese curso. Por favor especifica un curso válido.";
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }

        const respuesta = `El curso ${curso} vale ${knowledgeBase.cursos[curso].creditos} créditos.`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }

      // 4. Evaluación de expresiones lógicas
      else if (
        /Evalúa (.+)/i.test(pregunta) ||
        /Verifica (.+)/i.test(pregunta)
      ) {
        const expresion = pregunta
          .replace(/Evalúa /i, "")
          .replace(/Verifica /i, "")
          .replace(/\?/g, "")
          .trim();

        try {
          const resultado = this.evaluarExpresion(expresion);
          const respuesta = `La expresión "${expresion}" es ${
            resultado ? "verdadera" : "falsa"
          }.`;
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        } catch (e) {
          const respuesta =
            "No pude evaluar esa expresión. Asegúrate de usar AND, OR, NOT correctamente.";
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }
      }

      // 5. Preguntas combinadas (para probar inferencias)
      else if (/Si aprobé (.+), ¿puedo tomar (.+)\??/i.test(pregunta)) {
        const match = pregunta.match(/Si aprobé (.+), ¿puedo tomar (.+)\??/i);
        const cursoAprobadoInput = match ? match[1] : null;
        const cursoDeseadoInput = match ? match[2] : null;
        const cursoAprobado = cursoAprobadoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoAprobadoInput)
          : null;
        const cursoDeseado = cursoDeseadoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoDeseadoInput)
          : null;

        if (!cursoAprobado || !cursoDeseado) {
          const respuesta =
            "No entendí la pregunta. Por favor formula tu pregunta como: 'Si aprobé X, ¿puedo tomar Y?'";
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }

        const tempAprobados = [...this.cursosAprobados, cursoAprobado];
        const puedeTomar = knowledgeBase.reglas.puedeTomar(
          cursoDeseado,
          tempAprobados
        );
        const respuesta = puedeTomar
          ? `Sí, si apruebas ${cursoAprobado}, podrías tomar ${cursoDeseado}.`
          : `No, incluso aprobando ${cursoAprobado}, no podrías tomar ${cursoDeseado}. Requisitos faltantes: ${
              knowledgeBase.cursos[cursoDeseado].requisito || "ninguno"
            }`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      } else if (
        /¿Qué cursos puedo tomar si solo he aprobado (.+)\??/i.test(pregunta)
      ) {
        const match = pregunta.match(
          /¿Qué cursos puedo tomar si solo he aprobado (.+)\??/i
        );
        const cursoAprobadoInput = match ? match[1] : null;
        const cursoAprobado = cursoAprobadoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoAprobadoInput)
          : null;

        if (!cursoAprobado) {
          const respuesta =
            "No reconozco ese curso. Por favor especifica un curso válido.";
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }

        const tempAprobados = [cursoAprobado];
        const disponibles =
          knowledgeBase.reglas.cursosDisponibles(tempAprobados);

        if (disponibles.length === 0) {
          const respuesta = `Con solo ${cursoAprobado} aprobado, no hay cursos disponibles.`;
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        } else {
          const respuesta = `Con solo ${cursoAprobado} aprobado, puedes tomar: ${disponibles.join(
            ", "
          )}`;
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }
      }

      // 6. Manejo de errores
      else if (/Aprobé\s*$/i.test(pregunta)) {
        const respuesta =
          "Por favor especifica qué curso has aprobado. Ejemplo: 'Aprobé Programación I'";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      } else if (/Evalúa .* y .*/i.test(pregunta)) {
        const respuesta =
          "Para evaluar expresiones, usa 'AND' en lugar de 'y'. Ejemplo: 'Evalúa Programación I AND Matemáticas Discretas'";
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }

      // 7. Preguntas complejas
      else if (
        /Necesito saber si puedo tomar (.+) habiendo aprobado solo (.+)/i.test(
          pregunta
        )
      ) {
        const match = pregunta.match(
          /Necesito saber si puedo tomar (.+) habiendo aprobado solo (.+)/i
        );
        const cursoDeseadoInput = match ? match[1] : null;
        const cursoAprobadoInput = match ? match[2] : null;
        const cursoDeseado = cursoDeseadoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoDeseadoInput)
          : null;
        const cursoAprobado = cursoAprobadoInput
          ? knowledgeBase.reglas.buscarCursoPorNombre(cursoAprobadoInput)
          : null;

        if (!cursoDeseado || !cursoAprobado) {
          const respuesta =
            "No entendí la pregunta. Por favor formula tu pregunta como: 'Necesito saber si puedo tomar X habiendo aprobado solo Y'";
          this.historial.push(`Chatbot: ${respuesta}`);
          return respuesta;
        }

        const tempAprobados = [cursoAprobado];
        const puedeTomar = knowledgeBase.reglas.puedeTomar(
          cursoDeseado,
          tempAprobados
        );
        const respuesta = puedeTomar
          ? `Sí, habiendo aprobado solo ${cursoAprobado}, podrías tomar ${cursoDeseado}.`
          : `No, con solo ${cursoAprobado} aprobado, no podrías tomar ${cursoDeseado}. Requisitos faltantes: ${
              knowledgeBase.cursos[cursoDeseado].requisito || "ninguno"
            }`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }

      // Respuesta por defecto
      else {
        const respuesta = `No entendí tu pregunta. Puedo ayudarte con:
- Consultar requisitos de cursos: "¿Qué necesito para tomar Inteligencia Artificial?"
- Registrar cursos aprobados: "Aprobé Programación I"
- Consultar horarios y créditos: "¿Cuál es el horario de Bases de Datos?"
- Evaluar expresiones lógicas: "Evalúa Programación I AND Matemáticas Discretas"
- Preguntas condicionales: "Si aprobé Programación I, ¿puedo tomar Bases de Datos?"`;
        this.historial.push(`Chatbot: ${respuesta}`);
        return respuesta;
      }
    } catch (error) {
      const respuesta =
        "Ocurrió un error al procesar tu pregunta. Por favor intenta de nuevo.";
      this.historial.push(`Chatbot: ${respuesta}`);
      return respuesta;
    }
  }

  mostrarHistorial() {
    return this.historial.join("\n");
  }
}

// Ejecución de todas las pruebas específicas
function ejecutarTodasLasPruebas() {
  const bot = new Chatbot();
  console.log("=== PRUEBAS COMPLETAS ===");

  console.log("\n1. Preguntas sobre requisitos de cursos:");
  console.log(bot.procesarPregunta("¿Puedo tomar Ingeniería de Software?"));
  console.log(
    bot.procesarPregunta("¿Qué necesito para tomar Inteligencia Artificial?")
  );
  console.log(
    bot.procesarPregunta(
      "¿Puedo tomar Bases de Datos sin haber aprobado Programación I?"
    )
  );
  console.log(
    bot.procesarPregunta(
      "¿Cuáles son los requisitos para Matemáticas Discretas?"
    )
  );

  console.log("\n2. Registro de cursos aprobados:");
  console.log(bot.procesarPregunta("Aprobé Programación I"));
  console.log(bot.procesarPregunta("He aprobado Matemáticas Discretas"));
  console.log(bot.procesarPregunta("Registra que pasé Bases de Datos"));
  console.log(bot.procesarPregunta("Ya terminé Inteligencia Artificial"));

  console.log("\n3. Consulta de información académica:");
  console.log(bot.procesarPregunta("¿Cuál es el horario de Programación I?"));
  console.log(bot.procesarPregunta("¿Qué días se imparte Bases de Datos?"));
  console.log(
    bot.procesarPregunta("¿Cuántos créditos vale Inteligencia Artificial?")
  );
  console.log(bot.procesarPregunta("¿A qué hora es Ingeniería de Software?"));

  console.log("\n4. Evaluación de expresiones lógicas:");
  console.log(
    bot.procesarPregunta("Evalúa Programación I AND Matemáticas Discretas")
  );
  console.log(
    bot.procesarPregunta("Verifica Programación I OR Bases de Datos")
  );
  console.log(bot.procesarPregunta("Evalúa NOT Programación I"));
  console.log(
    bot.procesarPregunta(
      "Verifica Inteligencia Artificial AND NOT Matemáticas Discretas"
    )
  );
  console.log(
    bot.procesarPregunta(
      "Evalúa Programación I AND Bases de Datos AND Ingeniería de Software"
    )
  );

  console.log("\n5. Preguntas combinadas:");
  console.log("Caso 1:");
  console.log(bot.procesarPregunta("Aprobé Programación I"));
  console.log(bot.procesarPregunta("¿Puedo tomar Ingeniería de Software?"));

  bot.cursosAprobados = []; // Reset
  console.log("\nCaso 2:");
  console.log(bot.procesarPregunta("Aprobé Matemáticas Discretas"));
  console.log(bot.procesarPregunta("¿Puedo tomar Inteligencia Artificial?"));

  bot.cursosAprobados = []; // Reset
  console.log("\nCaso 3:");
  console.log(bot.procesarPregunta("Aprobé Programación I"));
  console.log(bot.procesarPregunta("Aprobé Matemáticas Discretas"));
  console.log(
    bot.procesarPregunta("Evalúa Programación I AND Matemáticas Discretas")
  );

  console.log("\n6. Preguntas para probar manejo de errores:");
  console.log(bot.procesarPregunta("¿Puedo tomar Astronomía Avanzada?"));
  console.log(
    bot.procesarPregunta("Evalúa Programación I Y Matemáticas Discretas")
  );
  console.log(bot.procesarPregunta("Horario de Física Cuántica"));
  console.log(bot.procesarPregunta("Aprobé"));

  console.log("\n7. Preguntas complejas:");
  console.log(
    bot.procesarPregunta(
      "Si aprobé Programación I, ¿puedo tomar Bases de Datos?"
    )
  );
  console.log(
    bot.procesarPregunta(
      "¿Qué cursos puedo tomar si solo he aprobado Programación I?"
    )
  );
  console.log(
    bot.procesarPregunta(
      "Necesito saber si puedo tomar Inteligencia Artificial habiendo aprobado solo Matemáticas Discretas"
    )
  );

  console.log("\n=== HISTORIAL COMPLETO ===");
  console.log(bot.mostrarHistorial());
}

ejecutarTodasLasPruebas();
const bot = new Chatbot();
