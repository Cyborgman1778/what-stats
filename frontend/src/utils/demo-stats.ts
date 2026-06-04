import type { ChatStatsPayload } from 'src/services/api/types';

interface DemoDay {
  date: Date;
  label: string;
  count: number;
}

function toRecord(entries: Array<[string, number]>) {
  return Object.fromEntries(entries);
}

function formatDay(date: Date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}

function formatMonth(date: Date) {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();

  return `${month}/${year}`;
}

function buildDemoDays() {
  const start = new Date(2024, 0, 1);
  const weekdayBoost = [80, 110, 135, 170, 230, 320, 260];
  const days: DemoDay[] = [];

  for (let index = 0; index < 96; index += 1) {
    const date = new Date(start);
    date.setDate(start.getDate() + index);

    const base = 95 + ((index * 37) % 145);
    const boost = weekdayBoost[date.getDay()] ?? 0;
    const eventSpike = index % 14 === 5 ? 190 : 0;
    const reunionSpike = index % 29 === 0 ? 260 : 0;

    days.push({
      date,
      label: formatDay(date),
      count: base + boost + eventSpike + reunionSpike
    });
  }

  return days;
}

function buildMessagesByUser(totalMessages: number) {
  const ana = Math.round(totalMessages * 0.29);
  const luis = Math.round(totalMessages * 0.22);
  const marta = Math.round(totalMessages * 0.18);
  const carlos = Math.round(totalMessages * 0.14);
  const nuria = Math.round(totalMessages * 0.11);
  const phone = totalMessages - ana - luis - marta - carlos - nuria;

  return {
    Ana: ana,
    Luis: luis,
    Marta: marta,
    Carlos: carlos,
    Nuria: nuria,
    '+34 612 34 56 78': phone
  };
}

function buildMessagesPerMonth(days: DemoDay[]) {
  const record: Record<string, number> = {};

  days.forEach((day) => {
    const key = formatMonth(day.date);
    record[key] = (record[key] ?? 0) + day.count;
  });

  return record;
}

function buildMessagesPerYear(days: DemoDay[]) {
  const record: Record<string, number> = {};

  days.forEach((day) => {
    const key = String(day.date.getFullYear());
    record[key] = (record[key] ?? 0) + day.count;
  });

  return record;
}

function buildTopMessagesPerDay(days: DemoDay[]) {
  return toRecord(
    [...days]
      .sort((a, b) => b.count - a.count)
      .slice(0, 10)
      .map((day) => [day.label, day.count])
  );
}

const demoDays = buildDemoDays();
const demoTotalMessages = demoDays.reduce((total, day) => total + day.count, 0);
const demoMessagesPerUser = buildMessagesByUser(demoTotalMessages);

const demoStats: ChatStatsPayload = {
  status: 'success',
  message: 'Demo de resultados cargada correctamente.',
  total_messages: demoTotalMessages,
  participants: Object.keys(demoMessagesPerUser),
  total_users: Object.keys(demoMessagesPerUser).length,
  n_messages_per_user: demoMessagesPerUser,
  hot_hours: {
    '00:00': 182,
    '01:00': 96,
    '02:00': 44,
    '03:00': 19,
    '04:00': 12,
    '05:00': 21,
    '06:00': 58,
    '07:00': 214,
    '08:00': 462,
    '09:00': 728,
    '10:00': 913,
    '11:00': 1048,
    '12:00': 1196,
    '13:00': 1375,
    '14:00': 1242,
    '15:00': 1084,
    '16:00': 1328,
    '17:00': 1715,
    '18:00': 2054,
    '19:00': 2382,
    '20:00': 2648,
    '21:00': 2311,
    '22:00': 1587,
    '23:00': 704
  },
  messages_per_day: toRecord(demoDays.map((day) => [day.label, day.count])),
  messages_per_month: buildMessagesPerMonth(demoDays),
  messages_per_year: buildMessagesPerYear(demoDays),
  top_messages_per_day: buildTopMessagesPerDay(demoDays),
  top_words: {
    plan: 842,
    cena: 731,
    jajaja: 690,
    reunion: 604,
    foto: 588,
    cafe: 541,
    finde: 526,
    cumple: 492,
    viaje: 468,
    equipo: 431,
    playa: 398,
    peli: 374,
    trabajo: 352,
    tarde: 331,
    casa: 307,
    domingo: 286,
    musica: 265,
    pizza: 249,
    ruta: 224,
    abrazo: 201,
    viernes: 184,
    autobus: 159,
    gracias: 143,
    lluvia: 122,
    prueba: 94
  },
  top_emojis: {
    '😂': 1298,
    '❤️': 884,
    '🔥': 731,
    '😍': 628,
    '👍': 584,
    '🥳': 462,
    '☕': 388,
    '🍕': 342,
    '😅': 319,
    '👏': 288,
    '🚀': 247,
    '🌊': 229,
    '🎉': 211,
    '🙌': 190,
    '😎': 173,
    '💪': 144,
    '😴': 118,
    '🤔': 97,
    '✅': 84,
    '📍': 63
  },
  longest_messages: [
    {
      Author: 'Marta',
      Message:
        'Resumen del plan: quedamos a las 18:30 en la estacion, compramos algo para cenar, vamos directos al mirador y luego decidimos si seguimos con la ruta corta o volvemos en bus segun el tiempo.',
      Length: 184
    },
    {
      Author: 'Ana',
      Message:
        'Me parece bien hacer la demo con todos los casos: dias con picos, meses distintos, palabras repetidas, emojis variados, mensajes largos y rachas para que se vea cada panel completo.',
      Length: 168
    },
    {
      Author: 'Luis',
      Message:
        'Si alguien llega tarde no pasa nada, pero avisad por aqui para reorganizar coches y no quedarnos esperando sin saber si falta una persona o si ya viene de camino.',
      Length: 153
    },
    {
      Author: 'Carlos',
      Message:
        'Tengo los billetes, la reserva y la lista de compra compartida; revisad que no falte nada porque despues sera mas complicado encontrar tienda abierta.',
      Length: 146
    },
    {
      Author: 'Nuria',
      Message:
        'Confirmo que llevo camara, bateria externa, mantel y vasos. Tambien puedo preparar una playlist tranquila para el viaje si nadie tiene otra propuesta.',
      Length: 141
    },
    {
      Author: '+34 612 34 56 78',
      Message:
        'Soy nuevo en el grupo, guardadme como Diego cuando podais. Me apunto al plan del sabado y puedo llevar bebidas si todavia hacen falta.',
      Length: 131
    },
    {
      Author: 'Ana',
      Message: 'Voto por pizza, cafe y paseo corto; si llueve hacemos plan de peli en casa.',
      Length: 73
    },
    {
      Author: 'Luis',
      Message: 'El domingo por la tarde revisamos fotos y elegimos las mejores para compartir.',
      Length: 75
    },
    {
      Author: 'Marta',
      Message: 'No olvideis cargar el movil antes de salir, que luego siempre falta bateria.',
      Length: 72
    },
    {
      Author: 'Carlos',
      Message: 'Llego en diez minutos. Pedid mesa si veis que se llena el sitio.',
      Length: 65
    }
  ],
  top_streaks: [
    {
      start: '2024-01-10',
      end: '2024-03-10',
      duration: 61
    },
    {
      start: '2024-02-12',
      end: '2024-03-04',
      duration: 22
    },
    {
      start: '2024-03-15',
      end: '2024-04-02',
      duration: 19
    },
    {
      start: '2024-01-03',
      end: '2024-01-18',
      duration: 16
    },
    {
      start: '2024-01-24',
      end: '2024-02-02',
      duration: 10
    }
  ]
};

export function createDemoChatStats(): ChatStatsPayload {
  return JSON.parse(JSON.stringify(demoStats)) as ChatStatsPayload;
}
