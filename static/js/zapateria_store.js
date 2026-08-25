/**
 * Zapatería Loribell — Engine de Store de Sesión Interactivo (sessionStorage)
 * Simula la persistencia del software de gestión de taller en vivo.
 */

const ZAPATERIA_SEED = {
    business: {
        name: "Zapatería Loribell",
        phone: "3518905152",
        whatsapp: "5493518905152",
        address: "Obispo Lascano 2963, Villa Cabrera, Córdoba",
        hours: "Lunes a Viernes 9:00 a 13:00 y 15:00 a 18:00 hs. Sábados 9:00 a 13:00 hs.",
    },
    protocol: [
        { icon: "fa-broom", title: "Calzado 100% Limpio", desc: "Sin tierra, barro ni suciedad en capellada o suela." },
        { icon: "fa-ring", title: "Sin Cordones", desc: "Retirar cordones antes de entregar en el mostrador." },
        { icon: "fa-shoe-prints", title: "Sin Plantillas", desc: "Retirar plantillas internas o anatomicas." }
    ],
    remitos: [
        {
            id: 10922,
            fecha: "25/08/2026",
            cliente: "Gabriel Bustos",
            telefono: "3518905152",
            calzado: "Zapatillas Deportivas Nike Air Max",
            categoria: "deportivo",
            especialista: "División Calzado Deportivo",
            trabajo: "Pegado estructural de suelín y costura de refuerzo lateral",
            precio: 18500,
            estado: "en_proceso", // "pendiente", "en_proceso", "listo", "entregado"
            foto: null,
            notas: "Entregado en local sin cordones ni plantillas."
        },
        {
            id: 10921,
            fecha: "24/08/2026",
            cliente: "Mariana Rossi",
            telefono: "3514432109",
            calzado: "Botas de Cuero Caña Alta Prüne",
            categoria: "cuero",
            especialista: "División Calzado Regular & Cuero",
            trabajo: "Cambio completo de cierres YKK y reemplazo de tapas de taco",
            precio: 24000,
            estado: "listo",
            foto: "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=600&q=80",
            notas: "Trabajo terminado impecable. Lista para retiro."
        },
        {
            id: 10920,
            fecha: "23/08/2026",
            cliente: "Carlos Gómez",
            telefono: "3519876543",
            calzado: "Zapatillas Running Adidas Ultraboost",
            categoria: "deportivo",
            especialista: "División Calzado Deportivo",
            trabajo: "Costura de puntera mesh y vulcanizado de talón",
            precio: 15000,
            estado: "entregado",
            foto: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=600&q=80",
            notas: "Retirado y abonado en efectivo."
        }
    ],
    insumos: [
        { id: 1, nombre: "Cuero Vacuno Flor (Marrón/Negro)", cantidad: 14.5, unidad: "m²", minimo: 5, estado: "ok" },
        { id: 2, nombre: "Pegamento Fortex Adhesivo de Contacto", cantidad: 2.2, unidad: "Lts", minimo: 3.5, estado: "bajo" },
        { id: 3, nombre: "Suelas de Goma Deportiva (Talles 36-44)", cantidad: 28, unidad: "pares", minimo: 10, estado: "ok" },
        { id: 4, nombre: "Hilo de Nylon Encerado 0.8mm", cantidad: 8, unidad: "carretes", minimo: 3, estado: "ok" },
        { id: 5, nombre: "Cierres Metálicos para Botas YKK 35cm", cantidad: 11, unidad: "unid", minimo: 15, estado: "critico" },
        { id: 6, nombre: "Cambrillons de Acero Reforzados", cantidad: 42, unidad: "unid", minimo: 20, estado: "ok" }
    ]
};

class ZapateriaStore {
    constructor() {
        this.storageKey = "ggs_zapateria_session_v1";
        this.init();
    }

    init() {
        const existing = sessionStorage.getItem(this.storageKey);
        if (!existing) {
            this.reset();
        }
    }

    getData() {
        try {
            const raw = sessionStorage.getItem(this.storageKey);
            return raw ? JSON.parse(raw) : JSON.parse(JSON.stringify(ZAPATERIA_SEED));
        } catch (e) {
            console.error("Error reading Zapatería store", e);
            return JSON.parse(JSON.stringify(ZAPATERIA_SEED));
        }
    }

    saveData(data) {
        try {
            sessionStorage.setItem(this.storageKey, JSON.stringify(data));
            window.dispatchEvent(new CustomEvent("zapateriaStateChanged", { detail: data }));
        } catch (e) {
            console.error("Error saving Zapatería store", e);
        }
    }

    reset() {
        this.saveData(JSON.parse(JSON.stringify(ZAPATERIA_SEED)));
    }

    getRemitos(categoria = "todos", estado = "todos") {
        const data = this.getData();
        return data.remitos.filter(r => {
            const matchCat = categoria === "todos" || r.categoria === categoria;
            const matchEst = estado === "todos" || r.estado === estado;
            return matchCat && matchEst;
        });
    }

    getRemitoById(id) {
        const data = this.getData();
        return data.remitos.find(r => r.id === parseInt(id));
    }

    crearRemito(nuevoData) {
        const data = this.getData();
        const nextId = data.remitos.length > 0 ? Math.max(...data.remitos.map(r => r.id)) + 1 : 10923;
        const now = new Date();
        const fechaStr = `${String(now.getDate()).padStart(2, '0')}/${String(now.getMonth() + 1).padStart(2, '0')}/${now.getFullYear()}`;
        
        const remito = {
            id: nextId,
            fecha: fechaStr,
            cliente: nuevoData.cliente,
            telefono: nuevoData.telefono || "3518905152",
            calzado: nuevoData.calzado,
            categoria: nuevoData.categoria || "deportivo",
            especialista: nuevoData.categoria === "cuero" ? "División Calzado Regular & Cuero" : "División Calzado Deportivo",
            trabajo: nuevoData.trabajo,
            precio: parseFloat(nuevoData.precio) || 0,
            estado: "pendiente",
            foto: null,
            notas: nuevoData.notas || "Remito cargado en local."
        };

        data.remitos.unshift(remito);
        this.saveData(data);
        return remito;
    }

    actualizarEstadoRemito(id, nuevoEstado, fotoUrl = null) {
        const data = this.getData();
        const idx = data.remitos.findIndex(r => r.id === parseInt(id));
        if (idx !== -1) {
            data.remitos[idx].estado = nuevoEstado;
            if (fotoUrl) {
                data.remitos[idx].foto = fotoUrl;
            }
            this.saveData(data);
            return data.remitos[idx];
        }
        return null;
    }

    generarMensajeWhatsApp(remitoId) {
        const remito = this.getRemitoById(remitoId);
        if (!remito) return "#";

        const data = this.getData();
        const biz = data.business;
        const phone = remito.telefono.replace(/\D/g, "");
        const waNum = phone.startsWith("54") ? phone : (phone.length === 10 ? "549" + phone : "5493518905152");

        let msg = `*Zapatería Loribell — Aviso de Trabajo Listo* 👟👢\n\n`;
        msg += `Hola *${remito.cliente}*! Te informamos que tu pedido ya está *LISTO PARA RETIRAR*.\n\n`;
        msg += `📋 *N° Remito:* #${remito.id}\n`;
        msg += `👟 *Calzado:* ${remito.calzado}\n`;
        msg += `🛠️ *Trabajo:* ${remito.trabajo}\n`;
        msg += `💰 *Monto a Abonar:* $${remito.precio.toLocaleString("es-AR")} ARS\n\n`;
        msg += `📍 *Retiro en:* ${biz.address}\n`;
        msg += `⏰ *Horarios:* ${biz.hours}\n`;
        if (remito.foto) {
            msg += `📷 *Foto del trabajo realizado:* ${remito.foto}\n`;
        }
        msg += `\n_¡Muchas gracias por confiar en Zapatería Loribell!_`;

        return `https://wa.me/${waNum}?text=${encodeURIComponent(msg)}`;
    }

    actualizarInsumo(id, delta) {
        const data = this.getData();
        const insumo = data.insumos.find(i => i.id === parseInt(id));
        if (insumo) {
            insumo.cantidad = Math.max(0, Math.round((insumo.cantidad + delta) * 10) / 10);
            if (insumo.cantidad <= insumo.minimo * 0.5) {
                insumo.estado = "critico";
            } else if (insumo.cantidad <= insumo.minimo) {
                insumo.estado = "bajo";
            } else {
                insumo.estado = "ok";
            }
            this.saveData(data);
        }
    }
}

window.zapateriaStore = new ZapateriaStore();
