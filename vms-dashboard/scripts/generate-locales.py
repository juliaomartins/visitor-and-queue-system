# -*- coding: utf-8 -*-
"""Emit the three dictionary files as pure ASCII TypeScript.

Non-ASCII is written as \\uXXXX escapes. TypeScript reads those natively, and an
ASCII file cannot be mangled by a shell, an editor or a transcoding step on the
way to review -- which is exactly what happened to the first version of these
files on this Windows machine.
"""
from pathlib import Path

ROOT = Path(r"C:\workplace\vms\vms-dashboard\lib\locales")

HEAD_EN = '''/**
 * English - the source of truth for every message in the dashboard.
 *
 * THIS FILE DEFINES THE KEY SET. `pt.ts` and `tet.ts` are typed as `Messages`,
 * so leaving a key out of either one is a TypeScript error rather than a screen
 * that silently falls back to English in front of a delegate. Adding a message
 * means adding it here first; the compiler then names what is missing.
 *
 * Keys are namespaced by where they appear, not by what they say. Two screens
 * that share a word in English still get their own key, because they can
 * diverge in Tetun, where the noun governs the verb.
 *
 * NON-ASCII IS WRITTEN AS \\uXXXX ESCAPES ON PURPOSE, and these files are
 * generated rather than hand-edited. The first version of them was written
 * through a shell heredoc on Windows and came back with "\\u00e7\\u00f5" turned
 * to mojibake -- invisible in a diff until it reaches a delegate. An ASCII file
 * cannot be transcoded by anything in the chain.
 *
 * `{name}` placeholders are filled by `t(key, { name })` - see `lib/i18n.tsx`.
 */
export const en = {'''

HEAD_PT = '''import type { Messages } from "./en";

/**
 * Portuguese - European, not Brazilian.
 *
 * Timor-Leste follows Lisbon: "ecra" not "tela", "utilizador" not "usuario",
 * "eliminar" not "excluir". The progressive is "a + infinitive", which is why
 * the busy states below read "A terminar sessao..." rather than the Brazilian
 * "Terminando...".
 *
 * Generated and escaped for the reason given in `en.ts`.
 */
export const pt: Messages = {'''

HEAD_TET = '''import type { Messages } from "./en";

/**
 * Tetun Dili, in the INL orthography.
 *
 * Portuguese loanwords are spelled the way Tetun spells them, not the way
 * Portuguese does: "akreditasaun" not "acreditacao", "relatoriu" not
 * "relatorio", "ekran" not "ecra". Getting this wrong is the usual way a Tetun
 * interface ends up reading as Portuguese with the accents knocked off.
 *
 * Nouns are not inflected for number. "sira" marks a plural only where the
 * count is the point, so a nav label naming a destination stays singular while
 * a list of people does not.
 *
 * WORTH A NATIVE READ. These are careful, but Tetun has real regional variation
 * and the event's own staff can check them faster than any dictionary.
 *
 * Generated and escaped for the reason given in `en.ts`.
 */
export const tet: Messages = {'''

TAIL_EN = '''} as const;

/** Every message key in the dashboard. */
export type MessageKey = keyof typeof en;

/**
 * The shape a translation has to satisfy.
 *
 * `Record<MessageKey, string>` rather than `typeof en`: the English values are
 * literal types, and a translation must be free to say something different
 * while still covering every key.
 */
export type Messages = Record<MessageKey, string>;
'''

# (key, en, pt, tet). A key starting with "//" opens a section.
M = [
    ("//shell", "", "", ""),
    ("nav.sections", "Sections", "Secções", "Seksaun sira"),
    ("nav.group.overview", "Overview", "Visão geral", "Vizaun jerál"),
    ("nav.group.accreditation", "Accreditation", "Acreditação", "Akreditasaun"),
    ("nav.group.operations", "Operations", "Operações", "Operasaun"),
    ("nav.dashboard", "Dashboard", "Painel", "Painél"),
    ("nav.dashboard.hint", "Arrivals and door health",
     "Chegadas e estado das portas", "Xegada no estadu odamatan"),
    ("nav.visitors", "Visitors", "Visitantes", "Vizitante sira"),
    ("nav.visitors.hint", "Register and issue badges",
     "Registar e emitir crachás", "Rejistu no fó sai kartaun"),
    ("nav.badges", "Badges", "Crachás", "Kartaun"),
    ("nav.badges.hint", "Print queue", "Fila de impressão", "Fila ba impresaun"),
    ("nav.devices", "Devices", "Dispositivos", "Aparellu sira"),
    ("nav.devices.hint", "Doors and screens", "Portas e ecrãs",
     "Odamatan no ekrán"),
    ("nav.reports", "Reports", "Relatórios", "Relatóriu"),
    ("nav.reports.hint", "Entrance log", "Registo de entradas", "Rejistu tama"),
    ("nav.expand", "Expand menu", "Expandir menu", "Loke menu"),
    ("nav.collapse", "Collapse menu", "Recolher menu", "Taka menu"),
    ("nav.signOut", "Sign out", "Terminar sessão", "Sai"),
    ("nav.signingOut", "Signing out\u2026", "A terminar sessão\u2026",
     "Sai hela\u2026"),
    ("nav.settings", "Settings", "Configurações", "Konfigurasaun"),
    ("nav.settings.hint", "Server and appearance", "Servidor e aparência",
     "Servidor no hahalok"),
    ("nav.silentDevices", "{count} device not checked in recently",
     "{count} dispositivo sem comunicar recentemente",
     "Aparellu {count} seidauk komunika"),
    ("shell.restoringSession", "Restoring session", "A restaurar sessão",
     "Restaura sesaun hela"),
    ("topbar.localTime", "Local time", "Hora local", "Oras lokál"),

    ("//preferences", "", "", ""),
    ("theme.toDark", "Switch to dark mode", "Mudar para modo escuro",
     "Troka ba modu nakukun"),
    ("theme.toLight", "Switch to light mode", "Mudar para modo claro",
     "Troka ba modu naroman"),
    ("theme.dark", "Dark", "Escuro", "Nakukun"),
    ("theme.light", "Light", "Claro", "Naroman"),
    ("language.label", "Language", "Idioma", "Lian"),
    ("language.choose", "Choose a language", "Escolher idioma", "Hili lian"),

    ("//login", "", "", ""),
    ("login.title", "Sign in", "Iniciar sessão", "Tama"),
    ("login.intro",
     "Administrator accounts only. Guards use a paired phone, and the lobby "
     "screen pairs itself.",
     "Apenas contas de administrador. Os seguranças usam um telemóvel "
     "emparelhado e o ecrã do átrio emparelha-se sozinho.",
     "Konta administradór deit. Seguransa sira uza telemóvel ne\u2019ebé pareia "
     "ona, no ekrán resepsaun pareia an rasik."),
    ("login.username", "Username", "Utilizador", "Naran uzuáriu"),
    ("login.password", "Password", "Palavra-passe", "Liafuan-xave"),
    ("login.submit", "Sign in", "Iniciar sessão", "Tama"),
    ("login.submitting", "Signing in\u2026", "A iniciar sessão\u2026",
     "Tama hela\u2026"),
    ("login.badCredentials", "That username and password did not match.",
     "O utilizador e a palavra-passe não coincidem.",
     "Naran uzuáriu ho liafuan-xave la hanesan."),
    ("login.failedStatus", "Sign-in failed (HTTP {status}).",
     "Falha ao iniciar sessão (HTTP {status}).",
     "La konsege tama (HTTP {status})."),
    ("login.unreachable",
     "Could not reach the server. Check that the backend is running.",
     "Não foi possível contactar o servidor. Verifique se o backend está a "
     "correr.",
     "La bele kontaktu servidór. Verifika se backend la\u2019o hela."),
    ("login.servingFrom", "Serving from", "A partir de", "Husi"),
    ("login.pitch",
     "Register a visitor, print their card, and watch every arrival land in "
     "one place \u2014 on your own network, with nothing leaving the building.",
     "Registe um visitante, imprima o crachá e veja todas as chegadas num só "
     "lugar \u2014 na sua própria rede, sem nada sair do edifício.",
     "Rejista vizitante, imprime nia kartaun, no haree xegada hotu iha fatin "
     "ida \u2014 iha ita-nia rede rasik, laiha buat ida sai husi edifísiu."),

    ("//errors", "", "", ""),
    ("error.unexpected", "Something went wrong.", "Ocorreu um erro.",
     "Iha erru ida."),
    ("error.fields", "Some fields need attention.", "Há campos por corrigir.",
     "Iha kampu balu presiza hadia."),
    ("error.visitorLoad", "That visitor could not be loaded.",
     "Não foi possível carregar este visitante.",
     "La bele karga vizitante ne\u2019e."),
    ("error.visitorRegister", "The visitor could not be registered.",
     "Não foi possível registar o visitante.",
     "La bele rejista vizitante ne\u2019e."),
    ("error.visitorSave", "The changes could not be saved.",
     "Não foi possível guardar as alterações.", "La bele rai mudansa sira."),
    ("error.visitorActivate", "The visitor could not be activated.",
     "Não foi possível ativar o visitante.",
     "La bele ativa vizitante ne\u2019e."),
    ("error.visitorDeactivate", "The visitor could not be deactivated.",
     "Não foi possível desativar o visitante.",
     "La bele dezativa vizitante ne\u2019e."),
    ("error.visitorDelete", "The visitor could not be deleted.",
     "Não foi possível eliminar o visitante.",
     "La bele hasai vizitante ne\u2019e."),

    ("//visitor list", "", "", ""),
    ("visitors.title", "Visitors", "Visitantes", "Vizitante sira"),
    ("visitors.subtitle", "Everyone registered for the event",
     "Todos os inscritos no evento",
     "Ema hotu ne\u2019eb\u00e9 rejista ba eventu"),
    ("visitors.search", "Search visitors", "Procurar visitantes",
     "Buka vizitante"),
    ("visitors.searchPlaceholder",
     "Name, organisation, country or badge serial",
     "Nome, organiza\u00e7\u00e3o, pa\u00eds ou n\u00famero do crach\u00e1",
     "Naran, organizasaun, nasaun ka n\u00fameru kartaun"),
    ("visitors.filterCategory", "Filter by category", "Filtrar por categoria",
     "Filtra tuir kategoria"),
    ("visitors.tab.all", "Everyone", "Todos", "Hotu"),
    ("visitors.tab.normal", "Normal", "Normal", "Norm\u00e1l"),
    ("visitors.tab.vip", "VIP", "VIP", "VIP"),
    ("visitors.exportTitle",
     "Everyone registered, with their photo and badge QR. Nothing is reissued.",
     "Todos os inscritos, com foto e QR do cartão. Nada é reemitido.",
     "Ema hotu ne’ebé rejista, ho foto no QR kartaun. La fó sai kartaun foun."),
    ("visitors.exporting", "Exporting\u2026", "A exportar\u2026",
     "Esporta hela\u2026"),
    ("visitors.export", "Export Excel", "Exportar Excel", "Esporta Excel"),
    ("visitors.exportFailed", "The roster could not be exported.",
     "N\u00e3o foi poss\u00edvel exportar a lista.", "La bele esporta lista."),
    ("visitors.register", "Register visitor", "Registar visitante",
     "Rejista vizitante"),
    ("visitors.refreshing", "Refreshing\u2026", "A atualizar\u2026",
     "Atualiza hela\u2026"),
    ("visitors.loadFailed", "Could not load visitors",
     "N\u00e3o foi poss\u00edvel carregar os visitantes",
     "La bele karga vizitante sira"),
    ("visitors.requestFailed",
     "The request failed before it reached the server.",
     "O pedido falhou antes de chegar ao servidor.",
     "Pedidu falla molok to\u2019o servid\u00f3r."),
    ("visitors.serverRejected", "The server rejected that request.",
     "O servidor rejeitou o pedido.", "Servid\u00f3r rejeita pedidu ne\u2019e."),
    ("visitors.noneMatch", "No one matches those filters",
     "Ningu\u00e9m corresponde a esses filtros",
     "Laiha ema ida tuir filtru sira ne\u2019e"),
    ("visitors.noneMatchBody", "Try a shorter search, or widen the category.",
     "Tente uma pesquisa mais curta ou alargue a categoria.",
     "Koko buka ho liafuan badak liu, ka loke kategoria."),
    ("visitors.empty", "No visitors yet", "Ainda n\u00e3o h\u00e1 visitantes",
     "Seidauk iha vizitante"),
    ("visitors.emptyBody", "Register the first visitor to issue a badge.",
     "Registe o primeiro visitante para emitir um crach\u00e1.",
     "Rejista vizitante primeiru atu f\u00f3 sai kartaun."),
    ("visitors.menu.edit", "Edit details", "Editar dados", "Edita dadus"),
    ("visitors.menu.deactivate", "Deactivate visitor", "Desativar visitante",
     "Dezativa vizitante"),
    ("visitors.menu.activate", "Activate visitor", "Ativar visitante",
     "Ativa vizitante"),
    ("visitors.menu.delete", "Delete permanently", "Eliminar definitivamente",
     "Hasai permanente"),
    ("visitors.status.deactivated", "Deactivated", "Desativado", "Dezativadu"),

    ("//deactivate dialog", "", "", ""),
    ("deactivate.title", "Deactivate {name}?", "Desativar {name}?",
     "Dezativa {name}?"),
    ("deactivate.body",
     "Badge {serial} stops working immediately. The next scan of it shows red "
     "at the door.",
     "O crachá {serial} deixa de funcionar de imediato. A próxima leitura "
     "mostra vermelho à porta.",
     "Kartaun {serial} para funsiona kedas. Leitura tuirmai sei mosu mean iha "
     "odamatan."),
    ("deactivate.point1", "They stay on the visitor list, marked deactivated.",
     "Continuam na lista de visitantes, marcados como desativados.",
     "Sira sei hela iha lista vizitante, ho marka dezativadu."),
    ("deactivate.point2", "Their scan history is kept.",
     "O histórico de leituras é mantido.",
     "Istória leitura sei rai nafatin."),
    ("deactivate.point3",
     "Reversible. Activating puts the same printed card back to work — "
     "there is nothing to reprint.",
     "Reversível. Ativar põe o mesmo cartão impresso a funcionar — não há "
     "nada para reimprimir.",
     "Bele fila fali. Ativa fó fila kartaun ne’ebé imprime ona ba servisu "
     "— laiha buat atu imprime fali."),
    ("deactivate.cancel", "Keep them active", "Manter ativo",
     "Rai ativu nafatin"),
    ("deactivate.confirm", "Deactivate", "Desativar", "Dezativa"),
    ("deactivate.pending", "Deactivating…", "A desativar…",
     "Dezativa hela…"),

    ("//purge dialog", "", "", ""),
    ("purge.warning", "Cannot be undone", "Não pode ser anulado",
     "La bele fila fali"),
    ("purge.title", "Delete {name} permanently?",
     "Eliminar {name} definitivamente?", "Hasai {name} permanente?"),
    ("purge.body",
     "This removes the registration and the visitor’s photo from the server. "
     "Deactivating is the reversible option; this is not it.",
     "Isto remove o registo e a fotografia do visitante do servidor. Desativar "
     "é a opção reversível; esta não é.",
     "Ne’e hasai rejistu no vizitante nia foto husi servidór. Dezativa mak "
     "opsaun ne’ebé bele fila fali; ida ne’e lae."),
    ("purge.scansUnknown",
     "Any scans of this badge stay in the entrance log but stop naming "
     "anybody.",
     "As leituras deste crachá permanecem no registo de entradas, mas deixam "
     "de identificar alguém.",
     "Leitura kartaun ne’e nian sei hela iha rejistu tama, maibé la naran ema "
     "ida ona."),
    ("purge.scansNone",
     "No scans are affected — this badge has never been presented.",
     "Nenhuma leitura é afetada — este crachá nunca foi apresentado.",
     "Laiha leitura ida afetadu — kartaun ne’e seidauk aprezenta."),
    ("purge.scansOne",
     "{count} scan stays in the entrance log but stops naming anybody.",
     "{count} leitura permanece no registo de entradas, mas deixa de "
     "identificar alguém.",
     "Leitura {count} sei hela iha rejistu tama, maibé la naran ema ida ona."),
    ("purge.scansMany",
     "{count} scans stay in the entrance log but stop naming anybody.",
     "{count} leituras permanecem no registo de entradas, mas deixam de "
     "identificar alguém.",
     "Leitura {count} sei hela iha rejistu tama, maibé la naran ema ida ona."),
    ("purge.serialRetired", "Badge {serial} is retired. The serial is not "
     "reused.",
     "O crachá {serial} é retirado. O número não é reutilizado.",
     "Kartaun {serial} hasai ona. Númeru ne’e la uza fali."),
    ("purge.reRegister",
     "Registering them again later creates a new visitor, a new serial and a "
     "new QR.",
     "Voltar a registá-los cria um novo visitante, um novo número e um novo QR.",
     "Rejista fila sira sei kria vizitante foun, númeru foun no QR foun."),
    ("purge.typeToConfirm", "Type {serial} to confirm",
     "Escreva {serial} para confirmar", "Hakerek {serial} atu konfirma"),
    ("purge.cancel", "Cancel", "Cancelar", "Kansela"),
    ("purge.confirm", "Delete permanently", "Eliminar definitivamente",
     "Hasai permanente"),
    ("purge.pending", "Deleting…", "A eliminar…", "Hasai hela…"),

    ("//visitor detail", "", "", ""),
    ("common.loading", "Loading…", "A carregar…", "Karga hela…"),
    ("visitor.fallbackTitle", "Visitor", "Visitante", "Vizitante"),
    ("visitor.notFound", "Could not load this visitor",
     "Não foi possível carregar este visitante",
     "La bele karga vizitante ne’e"),
    ("visitor.notFoundBody",
     "They may have been deleted. Check the visitor list.",
     "Pode ter sido eliminado. Consulte a lista de visitantes.",
     "Karik hasai tiha ona. Haree lista vizitante."),
    ("visitor.backToAll", "Back to all visitors",
     "Voltar a todos os visitantes", "Fila ba vizitante hotu"),
    ("visitor.allVisitors", "All visitors", "Todos os visitantes",
     "Vizitante hotu"),
    ("visitor.status.active", "Active", "Ativo", "Ativu"),
    ("visitor.headingActive", "This badge opens the door",
     "Este crachá abre a porta", "Kartaun ne’e loke odamatan"),
    ("visitor.headingOff", "This badge is switched off",
     "Este crachá está desligado", "Kartaun ne’e desliga ona"),
    ("visitor.subActive",
     "Any paired scanner will accept it and the lobby screen will welcome them.",
     "Qualquer leitor emparelhado aceita-o e o ecrã do átrio dá as "
     "boas-vindas.",
     "Leitór ne’ebé pareia ona sei simu, no ekrán resepsaun sei fó benvindu."),
    ("visitor.subOff",
     "The next scan of it shows red. Activating puts the same card back to "
     "work — nothing needs reprinting.",
     "A próxima leitura mostra vermelho. Ativar põe o mesmo cartão a funcionar "
     "— não é preciso reimprimir.",
     "Leitura tuirmai sei mosu mean. Ativa fó fila kartaun hanesan ba servisu "
     "— la presiza imprime fali."),
    ("visitor.registered", "Registered", "Registado", "Rejista"),
    ("visitor.arrivals", "Arrivals", "Chegadas", "Xegada"),
    ("visitor.lastArrival", "Last arrival", "Última chegada", "Xegada ikus"),
    ("visitor.notYet", "Not yet", "Ainda não", "Seidauk"),
    ("visitor.scansLogged", "Scans logged", "Leituras registadas",
     "Leitura rejistadu"),
    ("visitor.activating", "Activating…", "A ativar…", "Ativa hela…"),
    ("visitor.qrNote",
     "This QR was generated when the visitor was registered and never changes. "
     "Reprint the card as often as you need — it scans the same every time. "
     "Deactivating stops it and activating starts it again, both without "
     "touching the code on the card. Deleting permanently is the only thing "
     "here that cannot be undone.",
     "Este QR foi gerado no registo do visitante e nunca muda. Reimprima o "
     "cartão as vezes que precisar — lê-se sempre igual. Desativar para-o e "
     "ativar volta a pô-lo a funcionar, sem tocar no código do cartão. "
     "Eliminar definitivamente é a única coisa aqui que não pode ser anulada.",
     "QR ne’e kria bainhira rejista vizitante no nunka muda. Imprime fali "
     "kartaun dala hira mak presiza — nia lee hanesan beibeik. Dezativa para "
     "nia, no ativa hahú fali, rua ne’e la book kódigu iha kartaun. Hasai "
     "permanente mak buat ida deit iha ne’e ne’ebé la bele fila fali."),
    ("visitor.scanHistory", "Scan history", "Histórico de leituras",
     "Istória leitura"),
    ("visitor.scanHistoryBody",
     "Every time this badge was presented, including the times it was refused.",
     "Todas as vezes que este crachá foi apresentado, incluindo as recusadas.",
     "Dala hotu kartaun ne’e aprezenta, inklui dala ne’ebé rejeita."),
    ("visitor.noScans", "This badge has not been scanned yet.",
     "Este crachá ainda não foi lido.", "Kartaun ne’e seidauk lee."),
    ("visitor.col.event", "Event", "Evento", "Eventu"),
    ("visitor.col.scannedAt", "Scanned at", "Lido em", "Lee iha"),
    ("visitor.col.result", "Result", "Resultado", "Rezultadu"),
    ("visitor.col.device", "Device", "Dispositivo", "Aparellu"),
    ("scan.valid", "Valid", "Válido", "Válidu"),
    ("scan.duplicate", "Duplicate", "Duplicado", "Duplikadu"),
    ("scan.revoked", "Revoked", "Revogado", "Revogadu"),
    ("scan.invalid", "Invalid", "Inválido", "Inválidu"),

    ("//registration form", "", "", ""),
    ("register.title", "Register a visitor", "Registar um visitante",
     "Rejista vizitante ida"),
    ("register.subtitle",
     "One badge, printed in advance, valid for the whole event",
     "Um crachá, impresso com antecedência, válido para todo o evento",
     "Kartaun ida, imprime uluk, válidu ba eventu tomak"),
    ("register.issuedTitle", "Badge issued", "Crachá emitido",
     "Kartaun fó sai ona"),
    ("register.issuedSubtitle",
     "Print the card now, or from the visitor’s page later",
     "Imprima o cartão agora, ou mais tarde a partir da página do visitante",
     "Imprime kartaun agora, ka depois husi vizitante nia pájina"),
    ("form.photoRequired",
     "A badge needs a photo. Add one before registering.",
     "Um crachá precisa de uma fotografia. Adicione uma antes de registar.",
     "Kartaun presiza foto. Tau ida molok rejista."),
    ("form.fullName", "Full name", "Nome completo", "Naran kompletu"),
    ("form.fullNameHint", "As it should read on the badge.",
     "Como deve aparecer no crachá.",
     "Hanesan ne’ebé tenke mosu iha kartaun."),
    ("form.country", "Country", "País", "Nasaun"),
    ("form.organisation", "Organisation", "Organização", "Organizasaun"),
    ("form.optional", "Optional.", "Opcional.", "Opsionál."),
    ("form.category", "Category", "Categoria", "Kategoria"),
    ("form.cat.normal", "Normal", "Normal", "Normál"),
    ("form.cat.normalNote", "Standard badge", "Crachá normal",
     "Kartaun normál"),
    ("form.cat.vip", "VIP", "VIP", "VIP"),
    ("form.cat.vipNote", "Distinct card and lobby welcome",
     "Cartão distinto e boas-vindas no átrio",
     "Kartaun espesiál no benvindu iha resepsaun"),
    ("form.registering", "Registering…", "A registar…", "Rejista hela…"),
    ("form.saving", "Saving…", "A guardar…", "Rai hela…"),
    ("form.register", "Register and issue badge", "Registar e emitir crachá",
     "Rejista no fó sai kartaun"),
    ("form.save", "Save changes", "Guardar alterações", "Rai mudansa"),
    ("form.noteCreate",
     "The serial is assigned when you register. The QR is generated at the "
     "same moment and never changes afterwards.",
     "O número é atribuído no momento do registo. O QR é gerado nesse mesmo "
     "instante e nunca muda depois.",
     "Númeru fó bainhira rejista. QR kria iha momentu hanesan no nunka muda "
     "depois."),
    ("form.noteEdit",
     "Editing details does not reissue the badge. The serial and the QR code "
     "stay exactly as printed.",
     "Editar os dados não reemite o crachá. O número e o código QR ficam "
     "exatamente como foram impressos.",
     "Edita dadus la fó sai kartaun foun. Númeru no kódigu QR sei hanesan ho "
     "ne’ebé imprime ona."),

    ("//badge receipt", "", "", ""),
    ("receipt.badgeIssued", "Badge issued", "Crachá emitido",
     "Kartaun fó sai ona"),
    ("receipt.registered", "{name} is registered", "{name} está registado",
     "{name} rejista ona"),
    ("receipt.permanent",
     "This QR is permanent. It was generated when {name} was registered and "
     "will not change — print it now, or from their page later, as many times "
     "as you need. It only stops working if you deactivate or delete the "
     "visitor.",
     "Este QR é permanente. Foi gerado quando {name} foi registado e não muda "
     "— imprima-o agora, ou mais tarde a partir da página do visitante, as "
     "vezes que precisar. Só deixa de funcionar se desativar ou eliminar o "
     "visitante.",
     "QR ne’e permanente. Nia kria bainhira rejista {name} no sei la muda — "
     "imprime agora, ka depois husi nia pájina, dala hira mak presiza. Nia "
     "para funsiona deit se dezativa ka hasai vizitante."),
    ("receipt.qrAlt", "QR code for badge {serial}",
     "Código QR do crachá {serial}", "Kódigu QR ba kartaun {serial}"),
    ("receipt.badgeToken", "Badge token", "Token do crachá", "Token kartaun"),
    ("receipt.rendering", "Rendering…", "A gerar…", "Kria hela…"),
    ("receipt.downloadPdf", "Download badge PDF",
     "Transferir PDF do crachá", "Deskarrega PDF kartaun"),
    # Prints the server's PDF, not the page: the old browser-drawn card was the
    # wrong design and came out across five sheets.
    ("receipt.print", "Print badge", "Imprimir crachá", "Imprime kartaun"),
    ("receipt.printFellBack",
     "Pop-ups are blocked for this site, so the badge was downloaded instead. "
     "Open the file and print it from there.",
     "Os pop-ups estão bloqueados para este site, por isso o crachá foi "
     "transferido. Abra o ficheiro e imprima a partir daí.",
     "Pop-up bloke hela ba site ne’e, tan ne’e kartaun deskarrega ona. Loke "
     "fixeiru no imprime husi ne’ebá."),
    ("receipt.copied", "Copied", "Copiado", "Kopia ona"),
    ("receipt.copyToken", "Copy token", "Copiar token", "Kopia token"),
    ("receipt.qrFailed",
     "The QR code could not be drawn. Copy the token and print the badge from "
     "another machine rather than issuing a card without a code.",
     "Não foi possível desenhar o código QR. Copie o token e imprima o crachá "
     "noutra máquina, em vez de emitir um cartão sem código.",
     "La bele dezenha kódigu QR. Kopia token no imprime kartaun iha makina "
     "seluk, duke fó sai kartaun laiha kódigu."),
    ("receipt.copiedAnnounce", "Badge token copied to the clipboard.",
     "Token do crachá copiado para a área de transferência.",
     "Token kartaun kopia ba área transferénsia."),
    ("receipt.badgeSerial", "Badge serial", "Número do crachá",
     "Númeru kartaun"),
    ("receipt.registerAnother", "Register another visitor",
     "Registar outro visitante", "Rejista vizitante seluk"),
    ("receipt.open", "Open {name}", "Abrir {name}", "Loke {name}"),
    ("receipt.renderFailed", "The badge could not be rendered.",
     "Não foi possível gerar o crachá.", "La bele kria kartaun."),

    ("//edit", "", "", ""),
    ("edit.title", "Edit {name}", "Editar {name}", "Edita {name}"),
    ("edit.fallbackTitle", "Edit visitor", "Editar visitante",
     "Edita vizitante"),

    ("//photo upload and crop", "", "", ""),
    ("photo.label", "Photo", "Fotografia", "Foto"),
    # Numerals carry themselves; only the orientation is a word.
    ("photo.spec", "3:4 PORTRAIT · 600 × 800", "3:4 VERTICAL · 600 × 800",
     "3:4 VERTIKÁL · 600 × 800"),
    ("photo.notImage", "That is not an image. Choose a JPEG or PNG.",
     "Isso não é uma imagem. Escolha um JPEG ou PNG.",
     "Ne’e la’ós imajen. Hili JPEG ka PNG."),
    ("photo.tooLarge", "That image is over 20 MB. Choose a smaller one.",
     "Essa imagem tem mais de 20 MB. Escolha uma mais pequena.",
     "Imajen ne’e liu 20 MB. Hili ida ki’ik liu."),
    ("photo.alt", "The visitor’s badge photo",
     "A fotografia do crachá do visitante", "Vizitante nia foto kartaun"),
    ("photo.ready", "Cropped and ready.", "Recortada e pronta.",
     "Korta ona no prontu."),
    ("photo.onFile",
     "The photo already on file. It stays unless you replace it.",
     "A fotografia já guardada. Mantém-se a menos que a substitua.",
     "Foto ne’ebé rai ona. Nia sei hela to’o ita troka."),
    ("photo.adjustCrop", "Adjust crop", "Ajustar recorte", "Ajusta korta"),
    ("photo.chooseDifferent", "Choose a different photo",
     "Escolher outra fotografia", "Hili foto seluk"),
    ("photo.add", "Add a photo", "Adicionar fotografia", "Tau foto"),
    ("photo.dropHint",
     "Drop one here, or click to choose. You crop it next.",
     "Largue uma aqui, ou clique para escolher. A seguir recorta-a.",
     "Tau ida iha ne’e, ka klik atu hili. Tuirmai korta nia."),
    ("photo.dialogLabel", "Crop the visitor photo",
     "Recortar a fotografia do visitante", "Korta vizitante nia foto"),
    ("photo.frameFace", "Frame the face", "Enquadrar o rosto",
     "Tau oin iha kuadru"),
    ("photo.closeWithoutSaving", "Close without saving",
     "Fechar sem guardar", "Taka la rai"),
    ("crop.alt", "The photo being cropped", "A fotografia a ser recortada",
     "Foto ne’ebé korta hela"),
    ("crop.preview", "Cropped image", "Imagem recortada", "Imajen korta"),
    ("crop.circleHint",
     "Only the circle is printed and shown on the lobby screen. Fill it with "
     "the head and shoulders.",
     "Só o círculo é impresso e mostrado no ecrã do átrio. Preencha-o com a "
     "cabeça e os ombros.",
     "Sírkulu deit mak imprime no hatudu iha ekrán resepsaun. Tau ulun ho "
     "kabaas iha laran."),
    ("crop.aspect", "Aspect ratio", "Proporção", "Proporsaun"),
    ("crop.ratio.badge", "Badge (locked)", "Crachá (fixo)",
     "Kartaun (fiksu)"),
    ("crop.ratio.square", "Square", "Quadrado", "Kuadradu"),
    ("crop.ratio.free", "Free", "Livre", "Livre"),
    ("crop.width", "Width", "Largura", "Luan"),
    ("crop.height", "Height", "Altura", "Aas"),
    ("crop.heightLocked", "Height (locked)", "Altura (fixa)", "Aas (fiksu)"),
    ("crop.tooSmall",
     "This crop is {width}px wide. The badge prints the photo at {min}px for "
     "300dpi, so it will look soft on the card. Crop less, or use a larger "
     "photo.",
     "Este recorte tem {width}px de largura. O crachá imprime a fotografia a "
     "{min}px para 300dpi, por isso ficará desfocada no cartão. Recorte menos, "
     "ou use uma fotografia maior.",
     "Korta ne’e nia luan {width}px. Kartaun imprime foto ho {min}px ba "
     "300dpi, tan ne’e sei mosu la klaru iha kartaun. Korta uitoan deit, ka "
     "uza foto boot liu."),
    ("crop.quality", "Image quality", "Qualidade da imagem",
     "Kualidade imajen"),
    ("crop.bestCompression", "Best compression", "Mais compressão",
     "Kompresaun di’ak liu"),
    ("crop.bestQuality", "Best quality", "Mais qualidade",
     "Kualidade di’ak liu"),
    ("crop.applying", "Applying…", "A aplicar…", "Aplika hela…"),
    ("crop.use", "Use this photo", "Usar esta fotografia", "Uza foto ne’e"),
    ("crop.changeImage", "Change image", "Mudar de imagem", "Troka imajen"),

    ("//badges", "", "", ""),
    ("badges.title", "Badge printing", "Impressão de crachás",
     "Impresaun kartaun"),
    ("badges.subtitle", "Nine to an A4 sheet, with cut marks",
     "Nove por folha A4, com marcas de corte",
     "Sia iha folha A4 ida, ho marka korta"),
    ("badges.loadFailed", "The visitor list could not be loaded.",
     "Não foi possível carregar a lista de visitantes.",
     "La bele karga lista vizitante."),
    ("badges.safeTitle", "Printing is safe to repeat",
     "Imprimir de novo é seguro", "Imprime fali seguru"),
    ("badges.safeBody",
     "Every sheet carries each visitor’s existing QR, so a card can be "
     "reprinted as often as you need and the ones already handed out keep "
     "working. To stop a lost card, deactivate that visitor on their own page "
     "— the QR itself never changes, so activating them again puts the same "
     "card back to work.",
     "Cada folha leva o QR já existente de cada visitante, por isso um cartão "
     "pode ser reimpresso as vezes que precisar e os já entregues continuam a "
     "funcionar. Para travar um cartão perdido, desative esse visitante na "
     "página dele — o QR nunca muda, por isso ativá-lo de novo põe o mesmo "
     "cartão a funcionar.",
     "Folha ida-idak lori vizitante nia QR ne’ebé iha ona, tan ne’e kartaun "
     "bele imprime fali dala hira mak presiza no sira ne’ebé fó ona kontinua "
     "funsiona. Atu para kartaun lakon, dezativa vizitante ne’e iha nia "
     "pájina — QR nunka muda, tan ne’e ativa fali fó fila kartaun hanesan ba "
     "servisu."),
    ("badges.searchPlaceholder", "Name, organisation, country or serial",
     "Nome, organização, país ou número",
     "Naran, organizasaun, nasaun ka númeru"),
    ("badges.clearSelection", "Clear selection", "Limpar seleção",
     "Hamoos hili"),
    ("badges.selectAll", "Select all {count}", "Selecionar todos ({count})",
     "Hili hotu ({count})"),
    ("badges.print", "Print", "Imprimir", "Imprime"),
    ("badges.printCount", "Print {count}", "Imprimir {count}",
     "Imprime {count}"),
    ("badges.sheetFailed", "The sheet could not be produced.",
     "Não foi possível produzir a folha.", "La bele halo folha."),
    ("badges.export", "Export Excel", "Exportar Excel", "Esporta Excel"),
    ("badges.fileFailed", "The file could not be produced.",
     "Não foi possível produzir o ficheiro.", "La bele halo fixeiru."),
    ("badges.selectedOne", "{count} selected · {sheets} A4 sheet",
     "{count} selecionado · {sheets} folha A4",
     "{count} hili · folha A4 {sheets}"),
    ("badges.selectedMany", "{count} selected · {sheets} A4 sheets",
     "{count} selecionados · {sheets} folhas A4",
     "{count} hili · folha A4 {sheets}"),
    ("badges.noMatch", "No visitors match that search.",
     "Nenhum visitante corresponde a essa pesquisa.",
     "Laiha vizitante ida tuir buka ne’e."),
    ("badges.onSheet", "On the sheet", "Na folha", "Iha folha"),
    ("badges.notPrinting", "Not printing", "Fora da folha", "La imprime"),
    # The right-click menu on a card. One message per plural form, and the
    # heading exists only for many: a menu acting on one visitor names them.
    ("badges.menu.selection", "{count} selected visitors",
     "{count} visitantes selecionados", "Vizitante {count} ne’ebé hili"),
    ("badges.menu.printOne", "Print badge", "Imprimir crachá", "Imprime kartaun"),
    ("badges.menu.printMany", "Print {count} badges", "Imprimir {count} crachás",
     "Imprime kartaun {count}"),
    ("badges.menu.exportOne", "Export to Excel…", "Exportar para Excel…",
     "Esporta ba Excel…"),
    ("badges.menu.exportMany", "Export {count} to Excel…",
     "Exportar {count} para Excel…", "Esporta {count} ba Excel…"),

    ("//visitors list: source", "", "", ""),
    ("visitors.filterSource", "Filter by who registered",
     "Filtrar por quem registou", "Filtra tuir sé mak rejistu"),
    ("visitors.source.all", "Everyone", "Todos", "Hotu"),
    ("visitors.source.admin", "Desk", "Balcão", "Balkaun"),
    ("visitors.source.self", "Self-registered", "Autorregisto", "Rejistu rasik"),
    ("visitors.source.desk", "Walk-in desk", "Balcão de registo", "Meza rejistu"),
    ("visitors.possibleDuplicate", "Possible duplicate", "Possível duplicado",
     "Bele duplikadu"),
    ("visitors.possibleDuplicateTitle",
     "Another registration has the same name and country.",
     "Outro registo tem o mesmo nome e país.",
     "Rejistu seluk iha naran no nasaun hanesan."),

    ("//settings: public registration", "", "", ""),
    ("settings.registration", "Public registration", "Registo público",
     "Rejistu públiku"),
    ("settings.registrationNote",
     "Lets visitors register themselves from their phone on the event network. "
     "Each one is registered immediately with a normal badge.",
     "Permite que os visitantes se registem pelo telemóvel na rede do evento. "
     "Cada um fica registado de imediato com um crachá normal.",
     "Permite vizitante sira rejistu an rasik husi sira-nia telemóvel iha rede "
     "eventu nian. Ida-idak rejistu kedas ho kartaun normál."),
    ("settings.registrationToggle", "Allow public registration",
     "Permitir registo público", "Permite rejistu públiku"),
    ("settings.registrationOpen", "Open", "Aberto", "Loke"),
    ("settings.registrationClosed", "Closed", "Fechado", "Taka"),
    ("settings.registrationUrl", "Registration link", "Ligação de registo",
     "Link rejistu"),
    ("settings.registrationUrlNote",
     "Phones must be on the event Wi-Fi to open it.",
     "Os telemóveis têm de estar no Wi-Fi do evento para a abrir.",
     "Telemóvel tenke iha Wi-Fi eventu nian atu loke."),
    ("settings.registrationNoAddress",
     "The server's network address is not known yet.",
     "O endereço de rede do servidor ainda não é conhecido.",
     "Seidauk hatene enderesu rede servidór nian."),
    ("settings.registrationSaveFailed",
     "The switch could not be changed. Try again.",
     "Não foi possível alterar o interruptor. Tente novamente.",
     "La bele muda. Koko fali."),
    ("settings.registrationLoadFailed",
     "The server did not answer for this setting. If it was just updated, it needs a restart.",
     "O servidor não respondeu a esta definição. Se foi atualizado agora, tem de ser reiniciado.",
     "Servidór la hatán ba konfigurasaun ida-ne'e. Se foin atualiza, tenke hahú fali."),
    ("settings.registrationSaveQr", "Save QR code", "Guardar código QR",
     "Rai kódigu QR"),
    ("settings.registrationUpdated", "Last changed {time} by {user}",
     "Alterado pela última vez {time} por {user}",
     "Muda ikus iha {time} husi {user}"),

    ("//public registration page", "", "", ""),
    ("publicRegister.title", "Register for the event", "Registo no evento",
     "Rejistu ba eventu"),
    ("publicRegister.intro",
     "Fill in your details and add a photo. You will get a QR code to show at "
     "the entrance.",
     "Preencha os seus dados e adicione uma fotografia. Recebe um código QR para "
     "mostrar à entrada.",
     "Prienxe ita-nia dadus no aumenta foto ida. Ita sei simu kódigu QR ida atu "
     "hatudu iha entrada."),
    ("publicRegister.fullName", "Full name", "Nome completo", "Naran kompletu"),
    ("publicRegister.country", "Country", "País", "Nasaun"),
    ("publicRegister.countryPlaceholder", "Start typing your country",
     "Comece a escrever o seu país", "Hahú hakerek ita-nia nasaun"),
    # The country combobox, shared by the desk form and the public one.
    ("country.listLabel", "Countries", "Países", "Nasaun sira"),
    ("country.noMatch", "No countries match “{text}”",
     "Nenhum país corresponde a “{text}”",
     "La iha nasaun ne'ebé hanesan “{text}”"),
    ("country.invalid", "Select your country from the list.",
     "Selecione o seu país da lista.", "Hili ita-nia nasaun husi lista."),
    ("publicRegister.organization", "Organization (optional)",
     "Organização (opcional)", "Organizasaun (opsionál)"),
    ("publicRegister.photo", "Your photo", "A sua fotografia", "Ita-nia foto"),
    ("publicRegister.photoHint",
     "Face the camera in good light, with nobody else in the picture.",
     "Olhe para a câmara com boa luz, sem mais ninguém na imagem.",
     "Hateke ba kámara iha naroman di’ak, la iha ema seluk iha imajen."),
    ("publicRegister.choosePhoto", "Take or choose a photo",
     "Tirar ou escolher fotografia", "Foti ka hili foto"),
    ("publicRegister.useCamera", "Use the camera", "Usar a câmara", "Uza kámara"),
    ("publicRegister.capture", "Take photo", "Tirar fotografia", "Foti foto"),
    ("publicRegister.cancel", "Cancel", "Cancelar", "Kansela"),
    ("publicRegister.cameraFailed", "The camera could not be opened.",
     "Não foi possível abrir a câmara.", "La bele loke kámara."),
    ("publicRegister.changePhoto", "Change photo", "Mudar fotografia", "Muda foto"),
    # The photo review: a free crop with two round buttons over the photo.
    ("publicRegister.reviewPhoto", "Crop your photo", "Recorte a sua fotografia",
     "Tesi ita-nia foto"),
    ("publicRegister.usePhoto", "Use this photo", "Usar esta fotografia",
     "Uza foto ida-ne’e"),
    ("publicRegister.retakePhoto", "Take the photo again",
     "Tirar a fotografia novamente", "Foti foto fali"),
    ("publicRegister.cropTooSmall", "Too small to print. Drag the corners out.",
     "Demasiado pequena para imprimir. Arraste os cantos para fora.",
     "Ki’ik liu atu imprime. Dada kantu sira ba li’ur."),
    ("publicRegister.checkingFace", "Checking the photo…",
     "A verificar a fotografia…", "Verifika hela foto…"),
    ("publicRegister.faceNone",
     "No face found. Face the camera in good light and try again.",
     "Nenhum rosto encontrado. Olhe para a câmara com boa luz e tente novamente.",
     "La hetan oin. Hateke ba kámara iha naroman di’ak no koko fali."),
    ("publicRegister.faceMany",
     "More than one face found. Only you should be in the photo.",
     "Foi encontrado mais de um rosto. Só deve estar você na fotografia.",
     "Hetan oin liu ida. Tenke ita mesak de’it iha foto."),
    ("publicRegister.faceOk", "Photo looks good.", "A fotografia está boa.",
     "Foto di’ak."),
    ("publicRegister.consent",
     "Your photo and details are used for event access and deleted after the "
     "event.",
     "A sua fotografia e os seus dados são usados para o acesso ao evento e "
     "apagados depois do evento.",
     "Ita-nia foto no dadus uza ba asesu eventu nian no sei hamoos depois "
     "eventu."),
    ("publicRegister.submit", "Register", "Registar", "Rejistu"),
    ("publicRegister.submitting", "Registering…", "A registar…", "Rejistu hela…"),
    ("publicRegister.loading", "Loading…", "A carregar…", "Karrega hela…"),
    ("publicRegister.closedTitle", "Registration is closed", "O registo está fechado",
     "Rejistu taka ona"),
    ("publicRegister.closedBody", "Please go to the registration desk.",
     "Dirija-se ao balcão de registo.", "Favór ba balkaun rejistu."),
    ("publicRegister.unreachable",
     "The event server cannot be reached. Check that you are on the event Wi-Fi.",
     "Não é possível contactar o servidor do evento. Confirme que está no Wi-Fi "
     "do evento.",
     "La bele liga ba servidór eventu nian. Haree katak ita iha Wi-Fi eventu "
     "nian."),
    # The server answered, but not with the form's status -- a 404 from a
    # backend not yet restarted, or a 500. Not the visitor's Wi-Fi.
    ("publicRegister.unavailableTitle",
     "Registration is not available right now",
     "O registo não está disponível neste momento",
     "Rejistu la disponível agora"),
    ("publicRegister.failed",
     "Registration failed. Try again, or go to the registration desk.",
     "O registo falhou. Tente novamente ou dirija-se ao balcão de registo.",
     "Rejistu la susesu. Koko fali, ka ba balkaun rejistu."),
    ("publicRegister.tooMany",
     "Too many registrations from this connection. Please go to the "
     "registration desk.",
     "Demasiados registos a partir desta ligação. Dirija-se ao balcão de registo.",
     "Rejistu barak liu husi koneksaun ne’e. Favór ba balkaun rejistu."),
    ("publicRegister.tooLarge", "The photo is too large. Choose another one.",
     "A fotografia é demasiado grande. Escolha outra.",
     "Foto boot liu. Hili seluk."),
    ("publicRegister.successTitle", "You are registered", "Está registado",
     "Ita rejistu ona"),
    ("publicRegister.successShow", "Show this QR code at the entrance.",
     "Mostre este código QR à entrada.", "Hatudu kódigu QR ne’e iha entrada."),
    ("publicRegister.brightness", "Turn your screen brightness up before you scan.",
     "Aumente o brilho do ecrã antes de ler o código.",
     "Hasa’e naroman ekrán nian molok eskaneia."),
    ("publicRegister.deskHelp",
     "If the scan fails, go to the kiosk desk and quote {serial}.",
     "Se a leitura falhar, dirija-se ao balcão e indique {serial}.",
     "Se eskaneia la la’o, ba balkaun no temi {serial}."),
    ("publicRegister.keepPage", "Keep this page open until you are inside.",
     "Mantenha esta página aberta até entrar.",
     "Husik pájina ne’e loke to’o ita tama."),
    ("publicRegister.qrAlt", "QR code for badge {serial}",
     "Código QR do crachá {serial}", "Kódigu QR ba kartaun {serial}"),
    # The pass: saving the QR to the phone, and the switch closing mid-form.
    ("publicRegister.saveTitle", "Save it to your phone",
     "Guarde no seu telemóvel", "Rai iha ita-nia telemóvel"),
    ("publicRegister.saveBody",
     "Save the code so you still have it if this page closes.",
     "Guarde o código para o ter mesmo que esta página feche.",
     "Rai kódigu atu ita sei iha, maski pájina ne’e taka."),
    ("publicRegister.saveQr", "Save QR code", "Guardar código QR", "Rai kódigu QR"),
    ("publicRegister.savingQr", "Preparing…", "A preparar…", "Prepara hela…"),
    ("publicRegister.saveDone", "Saved to your phone.",
     "Guardado no seu telemóvel.", "Rai ona iha ita-nia telemóvel."),
    ("publicRegister.saveOpened",
     "Press and hold the image, then choose Save image.",
     "Toque sem soltar na imagem e escolha Guardar imagem.",
     "Kaer kleur imajen, depois hili Rai imajen."),
    ("publicRegister.saveFailed",
     "It could not be saved. Take a screenshot of this page instead.",
     "Não foi possível guardar. Faça uma captura de ecrã desta página.",
     "La bele rai. Foti kaptura ekrán husi pájina ne’e."),
    ("publicRegister.closedNow",
     "Registration has just closed. Go to the registration desk to finish.",
     "O registo acabou de fechar. Vá ao balcão de registo para terminar.",
     "Rejistu foin taka. Bá meza rejistu atu remata."),
    ("publicRegister.takePhoto", "Take a photo", "Tirar fotografia", "Foti foto"),
    ("publicRegister.chooseFromGallery", "Choose from gallery",
     "Escolher da galeria", "Hili husi galeria"),

    ("//export dialog", "", "", ""),
    ("export.titleOne", "Export badge codes for {count} visitor?",
     "Exportar códigos de crachá de {count} visitante?",
     "Esporta kódigu kartaun ba vizitante {count}?"),
    ("export.titleMany", "Export badge codes for {count} visitors?",
     "Exportar códigos de crachá de {count} visitantes?",
     "Esporta kódigu kartaun ba vizitante {count}?"),
    ("export.body",
     "This file contains a {strong} for every visitor in it. Nothing is "
     "changed by exporting — the codes are the ones already on their cards — "
     "but anyone holding the file can produce a badge that scans.",
     "Este ficheiro contém um {strong} para cada visitante nele. Exportar não "
     "altera nada — os códigos são os que já estão nos cartões — mas quem "
     "tiver o ficheiro consegue produzir um crachá que é lido.",
     "Fixeiru ne’e iha {strong} ba vizitante ida-idak. Esporta la muda buat "
     "ida — kódigu sira mak ne’ebé iha ona sira-nia kartaun — maibé ema "
     "ne’ebé iha fixeiru bele halo kartaun ne’ebé lee."),
    ("export.bodyStrong", "working QR code", "código QR funcional",
     "kódigu QR ne’ebé funsiona"),
    ("export.point1",
     "Send it the way you would send the printed cards, not the way you would "
     "send a guest list.",
     "Envie-o como enviaria os cartões impressos, não como enviaria uma lista "
     "de convidados.",
     "Haruka nia hanesan haruka kartaun imprimidu, la’ós hanesan haruka lista "
     "konvidadu."),
    ("export.point2",
     "Exporting again later produces an identical file. Losing this one costs "
     "nothing but the time to export it again.",
     "Exportar de novo mais tarde produz um ficheiro idêntico. Perder este só "
     "custa o tempo de o exportar outra vez.",
     "Esporta fali depois sei halo fixeiru hanesan. Lakon ida ne’e la kustu "
     "buat ida, tempu deit atu esporta fali."),
    ("export.point3",
     "To stop a specific badge, deactivate that visitor on their page. "
     "Deleting the file does not stop anything.",
     "Para travar um crachá específico, desative esse visitante na página "
     "dele. Apagar o ficheiro não trava nada.",
     "Atu para kartaun ida, dezativa vizitante ne’e iha nia pájina. Hasai "
     "fixeiru la para buat ida."),
    ("export.building", "Building…", "A preparar…", "Prepara hela…"),
    ("export.confirm", "Export and download", "Exportar e transferir",
     "Esporta no deskarrega"),

    # ------------------------------------------------------------ badge card --
    #
    # ONLY THE PARTS THAT ARE NOT PRINTED.
    #
    # components/badge-card.tsx mirrors what apps/badges/services.py draws with
    # ReportLab, and that is English: "Registered", "Country", "VIP GUEST" and
    # the visitor's role line are printed onto the physical card in Helvetica.
    # The preview exists to show what comes out of the printer, so translating
    # those labels would make it lie about the card -- the registrar would check
    # a Tetun preview and hand over an English badge.
    #
    # These two are screen-only: the deactivated overlay and the empty QR frame
    # never appear on a printed card, so they follow the interface instead.
    ("card.deactivated", "Deactivated", "Desativado", "Dezativadu"),
    ("card.qrOnCard", "on the printed card", "no cartão impresso",
     "iha kartaun imprimidu"),
    ("card.qrDrawing", "drawing…", "a desenhar…", "dezenha hela…"),
    ("card.qrFailed", "could not draw", "não foi possível desenhar",
     "la bele dezenha"),

    ("//devices", "", "", ""),
    ("time.justNow", "just now", "agora mesmo", "foin daudaun"),
    ("device.kind.scanner", "Scanner", "Leitor", "Leitór"),
    ("device.kind.screen", "Screen", "Ecrã", "Ekrán"),
    ("device.kind.desk", "Desk", "Balcão", "Meza"),
    # The same nouns mid-sentence, where English would lowercase them and the
    # other two would not necessarily agree about how.
    ("device.kindInline.scanner", "scanner", "leitor", "leitór"),
    ("device.kindInline.screen", "screen", "ecrã", "ekrán"),
    ("device.kindInline.desk", "desk", "balcão", "meza"),
    ("devices.subtitleQuiet", "Guard phones and the lobby screen",
     "Telemóveis dos seguranças e o ecrã do átrio",
     "Seguransa sira-nia telemóvel no ekrán resepsaun"),
    ("devices.silentOne", "{count} device has not checked in recently",
     "{count} dispositivo não comunica há algum tempo",
     "Aparellu {count} seidauk komunika"),
    ("devices.silentMany", "{count} devices have not checked in recently",
     "{count} dispositivos não comunicam há algum tempo",
     "Aparellu {count} seidauk komunika"),
    ("devices.alertOne", "{count} device is silent.",
     "{count} dispositivo está em silêncio.",
     "Aparellu {count} nonook."),
    ("devices.alertMany", "{count} devices are silent.",
     "{count} dispositivos estão em silêncio.",
     "Aparellu {count} nonook."),
    ("devices.alertBody",
     "A door with no scans in ten minutes is either quiet or offline — walk "
     "over and check.",
     "Uma porta sem leituras há dez minutos ou está parada ou está offline — "
     "vá lá verificar.",
     "Odamatan ne’ebé laiha leitura durante minutu sanulu karik nonook ka "
     "offline — bá haree."),
    ("devices.paired", "Paired devices", "Dispositivos emparelhados",
     "Aparellu ne’ebé pareia ona"),
    ("devices.pairedBody",
     "Refreshes on its own. “Last seen” is the last request a device made, so "
     "it is how you tell a quiet door from a dead phone.",
     "Atualiza sozinho. “Visto pela última vez” é o último pedido feito pelo "
     "dispositivo, e é assim que se distingue uma porta parada de um telemóvel "
     "morto.",
     "Atualiza an rasik. “Haree ikus” mak pedidu ikus ne’ebé aparellu halo, no "
     "ho ne’e mak ita hatene odamatan nonook ka telemóvel mate."),
    ("devices.loadFailed", "Could not load devices",
     "Não foi possível carregar os dispositivos", "La bele karga aparellu"),
    ("devices.none", "No devices paired yet",
     "Ainda não há dispositivos emparelhados", "Seidauk iha aparellu pareia"),
    ("devices.noneBody",
     "Generate a code above, then enter it on the guard’s phone or the lobby "
     "screen.",
     "Gere um código acima e introduza-o no telemóvel do segurança ou no ecrã "
     "do átrio.",
     "Kria kódigu iha leten, depois tau iha seguransa nia telemóvel ka ekrán "
     "resepsaun."),
    ("devices.col.device", "Device", "Dispositivo", "Aparellu"),
    ("devices.col.kind", "Kind", "Tipo", "Tipu"),
    ("devices.col.lastSeen", "Last seen", "Visto pela última vez",
     "Haree ikus"),
    ("devices.col.state", "State", "Estado", "Estadu"),
    ("devices.neverCheckedIn", "Never checked in", "Nunca comunicou",
     "Nunka komunika"),
    ("devices.silentCheck", "Silent — check the door",
     "Em silêncio — verifique a porta", "Nonook — haree odamatan"),
    ("devices.notSeenSincePairing", "Not seen since pairing",
     "Sem sinal desde o emparelhamento", "Laiha sinál desde pareia"),
    ("devices.stateRevoked", "REVOKED", "REVOGADO", "REVOGADU"),
    ("devices.stateActive", "ACTIVE", "ATIVO", "ATIVU"),
    ("devices.revoke", "Revoke", "Revogar", "Revoga"),

    ("//pairing", "", "", ""),
    ("pair.title", "Pair a device", "Emparelhar um dispositivo",
     "Pareia aparellu ida"),
    ("pair.body",
     "Open the app on the phone or screen, then read it the code below. Each "
     "code works once.",
     "Abra a aplicação no telemóvel ou no ecrã e leia-lhe o código abaixo. "
     "Cada código funciona uma só vez.",
     "Loke aplikasaun iha telemóvel ka ekrán, depois lee kódigu iha okos. "
     "Kódigu ida-idak funsiona dala ida deit."),
    ("pair.codeButton", "{kind} code", "Código de {kind}", "Kódigu {kind}"),
    ("pair.blurb.scanner", "A guard’s phone, at a door",
     "O telemóvel de um segurança, a uma porta",
     "Seguransa nia telemóvel, iha odamatan"),
    ("pair.blurb.screen", "The lobby display", "O ecrã do átrio",
     "Ekrán resepsaun"),
    ("pair.blurb.desk", "A laptop or tablet registering walk-ins at the door",
     "Um portátil ou tablet que regista visitantes à porta",
     "Laptop ka tablet ne’ebé rejista vizitante iha odamatan"),
    # The desk has no app to open, so its code comes with a link.
    ("pair.deskLink", "Desk link", "Ligação do balcão", "Link meza nian"),
    ("pair.deskLinkBody",
     "Open this on the desk device, then type the code above. It is shown here once.",
     "Abra isto no dispositivo do balcão e escreva o código acima. Só é mostrado aqui uma vez.",
     "Loke ne’e iha dispozitivu meza nian, depois hakerek kódigu iha leten. Hatudu de’it dala ida."),
    ("pair.deskLinkWarn",
     "Keep the link private. Anyone with the link and a code can register visitors.",
     "Mantenha a ligação privada. Quem tiver a ligação e um código pode registar visitantes.",
     "Rai link ne’e privadu. Ema ne’ebé iha link no kódigu bele rejista vizitante."),
    ("pair.deskLinkNoAddress", "The server network address is not known yet.",
     "O endereço de rede do servidor ainda não é conhecido.",
     "Seidauk hatene enderesu rede servidór nian."),
    ("pair.copyLink", "Copy link", "Copiar ligação", "Kopia link"),
    ("pair.copied", "Copied", "Copiado", "Kopia ona"),
    # The last resort, when even execCommand is refused: the text is selected.
    ("pair.copyManual", "Selected — press Ctrl+C to copy it.",
     "Selecionado — prima Ctrl+C para copiar.",
     "Hili ona — hanehan Ctrl+C atu kopia."),
    ("pair.codeLabel", "{kind} pairing code",
     "Código de emparelhamento de {kind}", "Kódigu pareia {kind}"),
    ("pair.expired",
     "This code has expired. Generate another — nothing was paired with it.",
     "Este código expirou. Gere outro — não foi emparelhado nada com ele.",
     "Kódigu ne’e liu ona tempu. Kria seluk — laiha buat ida pareia ho nia."),
    ("pair.expiresIn", "Expires in", "Expira em", "Liu tempu iha"),

    # ------------------------------------------------ the walk-in desk page
    ("desk.title", "Walk-in desk", "Balcão de registo", "Meza rejistu"),
    ("desk.pairTitle", "Pair this desk", "Emparelhar este balcão",
     "Pareia meza ne’e"),
    ("desk.pairBody",
     "Type the code from the dashboard. You only do this once on this device.",
     "Escreva o código do painel. Só faz isto uma vez neste dispositivo.",
     "Hakerek kódigu husi painel. Halo ida ne’e dala ida de’it iha dispozitivu ne’e."),
    ("desk.codeLabel", "Pairing code", "Código de emparelhamento", "Kódigu pareia"),
    ("desk.nameLabel", "Desk name", "Nome do balcão", "Naran meza"),
    ("desk.namePlaceholder", "Main entrance", "Entrada principal", "Entrada prinsipál"),
    ("desk.nameHint", "Where this desk stands. An admin sees it in the device list.",
     "Onde está este balcão. Um administrador vê-o na lista de dispositivos.",
     "Fatin meza ne’e. Administradór haree iha lista dispozitivu."),
    ("desk.pair", "Pair", "Emparelhar", "Pareia"),
    ("desk.pairing", "Pairing…", "A emparelhar…", "Pareia hela…"),
    ("desk.pairFailed", "That code was not accepted.",
     "Esse código não foi aceite.", "Kódigu ne’e la simu."),
    ("desk.formTitle", "Register a visitor", "Registar um visitante",
     "Rejista vizitante ida"),
    ("desk.fullName", "Full name", "Nome completo", "Naran kompletu"),
    ("desk.country", "Country", "País", "Nasaun"),
    ("desk.organization", "Organisation (optional)", "Organização (opcional)",
     "Organizasaun (opsionál)"),
    ("desk.category", "Badge type", "Tipo de crachá", "Tipu kartaun"),
    ("desk.normal", "Normal", "Normal", "Normál"),
    ("desk.vip", "VIP", "VIP", "VIP"),
    ("desk.photo", "Visitor photo", "Fotografia do visitante", "Foto vizitante nian"),
    ("desk.photoHint", "Take the photo, or choose one from this device.",
     "Tire a fotografia ou escolha uma deste dispositivo.",
     "Foti foto, ka hili ida husi dispozitivu ne’e."),
    ("desk.register", "Register visitor", "Registar visitante", "Rejista vizitante"),
    ("desk.registering", "Registering…", "A registar…", "Rejista hela…"),
    ("desk.doneTitle", "Registered", "Registado", "Rejista ona"),
    ("desk.showQr", "Ask the visitor to photograph this code.",
     "Peça ao visitante para fotografar este código.",
     "Husu vizitante atu foti foto kódigu ne’e."),
    ("desk.keepIt", "They show it at the entrance, today or tomorrow.",
     "Mostram-no à entrada, hoje ou amanhã.",
     "Sira hatudu iha entrada, ohin ka aban."),
    ("desk.again", "Register another visitor", "Registar outro visitante",
     "Rejista vizitante seluk"),
    # Staff can save the QR and send it on: the visitor may have no phone to hand.
    ("desk.downloadQr", "Download QR code", "Descarregar código QR",
     "Deskarega kódigu QR"),
    ("desk.downloading", "Preparing…", "A preparar…", "Prepara hela…"),
    ("desk.downloadDone", "Saved. Share it with the visitor.",
     "Guardado. Partilhe com o visitante.", "Rai ona. Fahe ba vizitante."),
    ("desk.downloadOpened", "Press and hold the image, then choose Save image.",
     "Toque sem soltar na imagem e escolha Guardar imagem.",
     "Kaer kleur imajen, depois hili Rai imajen."),
    ("desk.downloadFailed",
     "It could not be saved. Ask the visitor to photograph the code.",
     "Não foi possível guardar. Peça ao visitante para fotografar o código.",
     "La bele rai. Husu vizitante atu foti foto kódigu."),
    ("desk.qrAlt", "QR code for badge {serial}", "Código QR do crachá {serial}",
     "Kódigu QR ba kartaun {serial}"),
    ("desk.qrFailed", "The code could not be drawn. Register this visitor again.",
     "Não foi possível desenhar o código. Registe novamente este visitante.",
     "La bele dezeña kódigu. Rejista fali vizitante ne’e."),
    ("desk.unpaired", "This desk is no longer paired. Ask an admin for a new code.",
     "Este balcão já não está emparelhado. Peça um código novo a um administrador.",
     "Meza ne’e la pareia ona. Husu kódigu foun ba administradór."),
    ("desk.wrongDevice", "That code is for another kind of device.",
     "Esse código é para outro tipo de dispositivo.",
     "Kódigu ne’e ba dispozitivu tipu seluk."),
    ("desk.tooMany", "Too many registrations from this desk. Wait a few minutes.",
     "Demasiados registos deste balcão. Espere alguns minutos.",
     "Rejistu barak liu husi meza ne’e. Hein minutu balu."),
    ("desk.tooLarge", "The photo is too large. Choose another one.",
     "A fotografia é demasiado grande. Escolha outra.", "Foto boot liu. Hili seluk."),
    ("desk.failed", "The visitor could not be registered. Try again.",
     "Não foi possível registar o visitante. Tente novamente.",
     "La bele rejista vizitante. Koko fali."),
    ("desk.unreachable", "The event server cannot be reached.",
     "Não é possível contactar o servidor do evento.",
     "La bele kontaktu servidór eventu nian."),
    ("pair.alphabetNote",
     "Codes never contain 0, O, 1 or I — those four are left out because they "
     "are the ones people mishear and mistype. The device appears in the list "
     "below the moment it pairs.",
     "Os códigos nunca contêm 0, O, 1 nem I — esses quatro ficam de fora "
     "porque são os que as pessoas ouvem e escrevem mal. O dispositivo aparece "
     "na lista abaixo assim que emparelha.",
     "Kódigu nunka iha 0, O, 1 ka I — haat ne’e la tau tanba sira mak ema rona "
     "sala no hakerek sala. Aparellu mosu iha lista okos bainhira pareia."),

    ("//revoke device dialog", "", "", ""),
    ("revokeDevice.title", "Revoke {name}?", "Revogar {name}?",
     "Revoga {name}?"),
    ("revokeDevice.body",
     "This {kind} stops working {strong}. If it is a door phone, that door "
     "cannot record arrivals until someone re-pairs it.",
     "Este {kind} deixa de funcionar {strong}. Se for um telemóvel de porta, "
     "essa porta não consegue registar chegadas até alguém o emparelhar de "
     "novo.",
     "{kind} ne’e para funsiona {strong}. Se nia telemóvel odamatan nian, "
     "odamatan ne’e la bele rejista xegada to’o ema pareia fali."),
    ("revokeDevice.bodyStrong", "immediately", "de imediato", "kedas"),
    ("revokeDevice.point1",
     "{strong} — within seconds, without anyone walking over to it. Have a new "
     "pairing code ready if you mean to bring it straight back.",
     "{strong} — em segundos, sem ninguém ter de lá ir. Tenha um novo código "
     "de emparelhamento pronto se quiser trazê-lo logo de volta.",
     "{strong} — iha segundu balu, la presiza ema bá. Prepara kódigu pareia "
     "foun se ita hakarak lori nia fila kedas."),
    ("revokeDevice.point1Strong",
     "It drops back to its pairing screen on its own",
     "Volta sozinho ao ecrã de emparelhamento",
     "Nia fila mesak ba ekrán pareia"),
    ("revokeDevice.point2",
     "Its token is dead. There is no un-revoke — getting it back means a new "
     "pairing code.",
     "O seu token morreu. Não há forma de anular — recuperá-lo implica um novo "
     "código de emparelhamento.",
     "Nia token mate ona. Laiha dalan atu fila fali — atu hetan nia fali "
     "presiza kódigu pareia foun."),
    ("revokeDevice.point3",
     "Scans it already recorded are kept, and any it saved offline will still "
     "sync once it is paired again.",
     "As leituras que já registou são mantidas, e as que guardou offline ainda "
     "sincronizam quando voltar a emparelhar.",
     "Leitura ne’ebé nia rejista ona sei rai, no sira ne’ebé nia rai offline "
     "sei sinkroniza bainhira pareia fali."),
    ("revokeDevice.point4",
     "It stays in this list, marked revoked, so the audit trail holds.",
     "Permanece nesta lista, marcado como revogado, para o registo de "
     "auditoria se manter.",
     "Nia sei hela iha lista ne’e, ho marka revogadu, atu rejistu auditoria "
     "nafatin."),
    ("revokeDevice.cancel", "Keep it active", "Manter ativo",
     "Rai ativu nafatin"),
    ("revokeDevice.pending", "Revoking…", "A revogar…", "Revoga hela…"),
    ("revokeDevice.confirm", "Revoke device", "Revogar dispositivo",
     "Revoga aparellu"),

    ("error.deviceLoad", "The device list could not be loaded.",
     "Não foi possível carregar a lista de dispositivos.",
     "La bele karga lista aparellu."),
    ("error.pairingCode", "A pairing code could not be generated.",
     "Não foi possível gerar um código de emparelhamento.",
     "La bele kria kódigu pareia."),
    ("error.deviceRevoke", "The device could not be revoked.",
     "Não foi possível revogar o dispositivo.", "La bele revoga aparellu."),

    ("//reports", "", "", ""),
    ("reports.title", "Entrance log", "Registo de entradas", "Rejistu tama"),
    ("reports.subtitleQuiet", "Arrivals and refusals",
     "Chegadas e recusas", "Xegada no rejeisaun"),
    ("reports.subtitleRefused", "{count} refused at the door",
     "{count} recusados à porta", "{count} rejeita iha odamatan"),
    ("reports.subtitleNoRefusals", "No badges refused in this range",
     "Nenhum crachá recusado neste intervalo",
     "Laiha kartaun rejeita iha períodu ne’e"),
    ("reports.allOutcomes", "All outcomes", "Todos os resultados",
     "Rezultadu hotu"),
    ("reports.allCategories", "All categories", "Todas as categorias",
     "Kategoria hotu"),
    ("reports.from", "From", "De", "Husi"),
    ("reports.to", "To", "Até", "To’o"),
    ("reports.outcome", "Outcome", "Resultado", "Rezultadu"),
    ("reports.any", "Any", "Qualquer", "Ida-idak"),
    ("reports.exportNote",
     "Whatever the filters above are set to, exactly as shown.",
     "Exatamente como os filtros acima estão definidos.",
     "Tuir duni filtru sira iha leten, hanesan hatudu."),
    ("reports.preparing", "Preparing…", "A preparar…", "Prepara hela…"),
    ("reports.exportFailed", "The export could not be saved.",
     "Não foi possível guardar a exportação.", "La bele rai esportasaun."),
    ("reports.logFailed", "Could not load the log",
     "Não foi possível carregar o registo", "La bele karga rejistu"),
    ("reports.everyBadge", "Every badge presented",
     "Todos os crachás apresentados", "Kartaun hotu ne’ebé aprezenta"),
    ("reports.everyBadgeNote",
     "The rows behind the figures above, refusals included",
     "As linhas por trás dos números acima, recusas incluídas",
     "Liña sira iha númeru leten nia kotuk, inklui rejeisaun"),
    ("reports.timezone", "Times shown in {zone}.",
     "Horas mostradas em {zone}.", "Oras hatudu iha {zone}."),
    ("reports.format.pdf", "PDF report", "Relatório PDF", "Relatóriu PDF"),
    ("reports.format.pdfHint",
     "The written report — findings, charts and tables. For sending on.",
     "O relatório escrito — conclusões, gráficos e tabelas. Para reencaminhar.",
     "Relatóriu hakerek — deskoberta, gráfiku no tabela. Atu haruka ba."),
    ("reports.format.xlsx", "Excel workbook", "Livro Excel",
     "Livru Excel"),
    ("reports.format.xlsxHint",
     "Six sheets, figures as numbers. For anyone who wants to pivot it.",
     "Seis folhas, valores como números. Para quem quiser trabalhá-los.",
     "Folha neen, valór hanesan númeru. Ba ema ne’ebé hakarak halo análize."),
    ("reports.format.csv", "CSV log", "Registo CSV", "Rejistu CSV"),
    ("reports.format.csvHint",
     "The raw scan log, one row per badge presented. No analysis.",
     "O registo bruto de leituras, uma linha por crachá apresentado. Sem "
     "análise.",
     "Rejistu leitura krua, liña ida ba kartaun ida-idak. Laiha análize."),
    ("reports.export.stale",
     "That export is not available on the server yet — it is running an older "
     "build than this page. Restart the backend and try again.",
     "Essa exportação ainda não existe no servidor — está a correr uma versão "
     "mais antiga do que esta página. Reinicie o backend e tente de novo.",
     "Esportasaun ne’e seidauk iha servidór — nia la’o versaun tuan liu duke "
     "pájina ne’e. Hahú fali backend no koko fali."),
    ("reports.export.expired",
     "Your session expired. Reload the page and sign in again.",
     "A sua sessão expirou. Recarregue a página e inicie sessão de novo.",
     "Ita-nia sesaun liu tempu ona. Karga fali pájina no tama fali."),
    ("reports.export.serverError",
     "The server could not build that export (HTTP {status}).",
     "O servidor não conseguiu produzir essa exportação (HTTP {status}).",
     "Servidór la konsege halo esportasaun ne’e (HTTP {status})."),
    ("reports.export.downloadFailed",
     "That export could not be downloaded (HTTP {status}).",
     "Não foi possível transferir essa exportação (HTTP {status}).",
     "La bele deskarrega esportasaun ne’e (HTTP {status})."),
    ("error.reportLoad", "The entrance log could not be loaded.",
     "Não foi possível carregar o registo de entradas.",
     "La bele karga rejistu tama."),

    ("//recap", "", "", ""),
    ("recap.unavailable", "Analysis unavailable", "Análise indisponível",
     "Análize la disponivel"),
    ("recap.unavailableBody",
     "The server answered without the derived findings, which means it is "
     "running an older build than this page. Restart the backend and reload — "
     "the log below is unaffected and still accurate.",
     "O servidor respondeu sem as conclusões derivadas, o que significa que "
     "está a correr uma versão mais antiga do que esta página. Reinicie o "
     "backend e recarregue — o registo abaixo não é afetado e continua exato.",
     "Servidór hatán laiha deskoberta derivadu, katak nia la’o versaun tuan "
     "liu duke pájina ne’e. Hahú fali backend no karga fali — rejistu iha okos "
     "la afetadu no loos nafatin."),
    ("recap.scans", "Scans", "Leituras", "Leitura"),
    ("recap.inRange", "In this range", "Neste intervalo", "Iha períodu ne’e"),
    ("recap.people", "People", "Pessoas", "Ema"),
    ("recap.distinct", "Distinct visitors", "Visitantes distintos",
     "Vizitante la hanesan"),
    ("recap.duplicates", "Duplicates", "Duplicados", "Duplikadu"),
    ("recap.reEntries", "Re-entries, not refusals",
     "Reentradas, não recusas", "Tama fali, la’ós rejeisaun"),
    ("recap.refused", "Refused", "Recusados", "Rejeita"),
    ("recap.invalidOrRevoked", "Invalid or revoked",
     "Inválidos ou revogados", "Inválidu ka revogadu"),
    ("recap.nothingScanned", "Nothing scanned in this range",
     "Nada lido neste intervalo", "Laiha buat lee iha períodu ne’e"),
    ("recap.nothingScannedBody",
     "Widen the dates, or clear the filters. There is nothing to report on "
     "yet.",
     "Alargue as datas, ou limpe os filtros. Ainda não há nada para relatar.",
     "Loke loron barak liu, ka hamoos filtru. Seidauk iha buat atu relata."),
    ("recap.attendance", "Attendance", "Presença", "Prezensa"),
    ("recap.attendanceNote", "{arrived} of {registered} registered",
     "{arrived} de {registered} registados",
     "{arrived} husi {registered} rejista"),
    ("recap.scansLogged", "Scans logged", "Leituras registadas",
     "Leitura rejistadu"),
    ("recap.repeatNote", "{count} people came through more than once",
     "{count} pessoas passaram mais do que uma vez",
     "Ema {count} liu dala liu ida"),
    ("recap.busiestHour", "Busiest hour", "Hora de maior movimento",
     "Oras besik liu"),
    ("recap.peakNote", "{total} scans · {share}% of the period",
     "{total} leituras · {share}% do período",
     "Leitura {total} · {share}% husi períodu"),
    ("recap.noArrivals", "No arrivals recorded",
     "Nenhuma chegada registada", "Laiha xegada rejistadu"),
    ("recap.refusalNote", "{rate}% of everything presented",
     "{rate}% de tudo o que foi apresentado",
     "{rate}% husi buat hotu ne’ebé aprezenta"),
    ("recap.noneTurnedAway", "No badge turned away",
     "Nenhum crachá recusado", "Laiha kartaun rejeita"),
    ("recap.whatNumbersSay", "What the numbers say", "O que dizem os números",
     "Númeru sira hatete saida"),
    ("recap.whatNumbersSayNote",
     "Generated from this range — every line is a claim the data supports",
     "Gerado a partir deste intervalo — cada linha é uma afirmação que os "
     "dados sustentam",
     "Kria husi períodu ne’e — liña ida-idak mak afirmasaun ne’ebé dadus "
     "sustenta"),
    ("recap.loadByDoor", "Load by door", "Movimento por porta",
     "Movimentu tuir odamatan"),
    ("recap.loadByDoorNote",
     "One door turning away badges is a door with a problem",
     "Uma porta que recusa crachás é uma porta com um problema",
     "Odamatan ida ne’ebé rejeita kartaun mak odamatan ho problema"),
    ("recap.noDoorScan", "No door recorded a scan.",
     "Nenhuma porta registou leituras.", "Laiha odamatan rejista leitura."),
    ("recap.refusedHere", "{count} refused here", "{count} recusados aqui",
     "{count} rejeita iha ne’e"),
    ("recap.notArrived", "Registered, not yet arrived",
     "Registados, ainda não chegaram", "Rejista ona, seidauk to’o"),
    ("recap.notArrivedCount", "{count} of {registered}",
     "{count} de {registered}", "{count} husi {registered}"),
    ("recap.notArrivedNote",
     "No valid scan in this range. Full list is in the PDF and the workbook.",
     "Sem leitura válida neste intervalo. A lista completa está no PDF e no "
     "livro Excel.",
     "Laiha leitura válidu iha períodu ne’e. Lista kompletu iha PDF no livru "
     "Excel."),
    ("recap.andMore", "and {count} more", "e mais {count}",
     "no {count} tan"),

    ("//entry log", "", "", ""),
    ("entry.emptyBody", "Widen the dates, or clear the filters.",
     "Alargue as datas, ou limpe os filtros.",
     "Loke loron barak liu, ka hamoos filtru."),
    ("entry.col.time", "Time", "Hora", "Oras"),
    ("entry.col.name", "Name", "Nome", "Naran"),
    ("chart.noScans",
     "No scans in this range, so there is nothing to plot.",
     "Sem leituras neste intervalo, por isso não há nada para representar.",
     "Laiha leitura iha períodu ne’e, tan ne’e laiha buat atu hatudu."),
    ("chart.refused", "Refused", "Recusados", "Rejeita"),
    ("chart.scansByHour", "Scans by hour", "Leituras por hora",
     "Leitura tuir oras"),

    ("//overview", "", "", ""),
    ("overview.subtitleQuiet", "Today’s arrivals across every door",
     "As chegadas de hoje em todas as portas",
     "Ohin nia xegada iha odamatan hotu"),
    ("overview.silentOne", "{count} door has gone quiet — check Devices",
     "{count} porta ficou em silêncio — verifique Dispositivos",
     "Odamatan {count} nonook ona — haree Aparellu sira"),
    ("overview.silentMany", "{count} doors have gone quiet — check Devices",
     "{count} portas ficaram em silêncio — verifique Dispositivos",
     "Odamatan {count} nonook ona — haree Aparellu sira"),
    ("overview.registered", "Registered", "Registados", "Rejista"),
    ("overview.vipCount", "{count} VIP", "{count} VIP", "{count} VIP"),
    ("overview.arrivedToday", "Arrived today", "Chegaram hoje",
     "To’o ohin"),
    ("overview.arrivedNote", "{percent}% of those registered",
     "{percent}% dos registados", "{percent}% husi sira ne’ebé rejista"),
    ("overview.refusedAtDoor", "Refused at the door", "Recusados à porta",
     "Rejeita iha odamatan"),
    ("overview.duplicateOne", "{count} duplicate scan not counted",
     "{count} leitura duplicada não contada",
     "Leitura duplikadu {count} la konta"),
    ("overview.duplicateMany", "{count} duplicate scans not counted",
     "{count} leituras duplicadas não contadas",
     "Leitura duplikadu {count} la konta"),
    ("overview.doorsReporting", "Doors reporting", "Portas a comunicar",
     "Odamatan ne’ebé komunika"),
    ("overview.silentCount", "{count} silent", "{count} em silêncio",
     "{count} nonook"),
    ("overview.allCheckedIn", "All checked in recently",
     "Todas comunicaram recentemente", "Hotu komunika foin lalais"),
    ("overview.arrivalsByHour", "Arrivals by hour", "Chegadas por hora",
     "Xegada tuir oras"),
    ("overview.arrivalsByHourNote",
     "Every badge presented today, plotted where it happened",
     "Todos os crachás apresentados hoje, marcados na hora em que aconteceu",
     "Kartaun hotu ne’ebé aprezenta ohin, marka iha oras ne’ebé akontese"),
    ("overview.scanCountOne", "{count} scan", "{count} leitura",
     "leitura {count}"),
    ("overview.scanCountMany", "{count} scans", "{count} leituras",
     "leitura {count}"),
    ("overview.outcomeSplit", "Outcome split", "Divisão dos resultados",
     "Divizaun rezultadu"),
    ("overview.outcomeSplitNote", "How today’s scans divided",
     "Como se dividiram as leituras de hoje",
     "Oinsá ohin nia leitura fahe"),
    ("overview.recentScans", "Recent scans", "Leituras recentes",
     "Leitura foun sira"),
    ("overview.recentScansNote", "Newest first, refusals included",
     "Mais recentes primeiro, recusas incluídas",
     "Foun liu uluk, inklui rejeisaun"),
    ("overview.nothingToday", "Nothing has been scanned yet today.",
     "Ainda não foi lido nada hoje.", "Ohin seidauk lee buat ida."),
    ("overview.arrivalsAppear",
     "Arrivals appear here the moment a guard scans a badge.",
     "As chegadas aparecem aqui assim que um segurança lê um crachá.",
     "Xegada mosu iha ne’e bainhira seguransa lee kartaun."),
    ("overview.colVisitor", "Visitor", "Visitante", "Vizitante"),
    ("overview.openLog", "Open the full entrance log →",
     "Abrir o registo de entradas completo →",
     "Loke rejistu tama kompletu →"),
    # Two counts in one sentence, so all four combinations get their own
    # message. Portuguese conjugates the verb for the first and agrees the noun
    # with the second; assembling it from fragments cannot produce that.
    ("overview.arrivedSummary.oneOne",
     "{people} person has arrived across {scans} scan.",
     "{people} pessoa chegou em {scans} leitura.",
     "Ema {people} to’o ho leitura {scans}."),
    ("overview.arrivedSummary.oneMany",
     "{people} person has arrived across {scans} scans.",
     "{people} pessoa chegou em {scans} leituras.",
     "Ema {people} to’o ho leitura {scans}."),
    ("overview.arrivedSummary.manyOne",
     "{people} people have arrived across {scans} scan.",
     "{people} pessoas chegaram em {scans} leitura.",
     "Ema {people} to’o ho leitura {scans}."),
    ("overview.arrivedSummary.manyMany",
     "{people} people have arrived across {scans} scans.",
     "{people} pessoas chegaram em {scans} leituras.",
     "Ema {people} to’o ho leitura {scans}."),

    ("//brand", "", "", ""),
    # No article before the placeholders. English wants "the", Portuguese wants
    # "pelo" or "pela" depending on the organiser's gender, and the organisers
    # are configuration rather than message keys -- so the sentence is written
    # to need neither.
    ("brand.organisedBy", "Organised by {first} and {second}.",
     "Organizado por {first} e {second}.",
     "Organiza husi {first} no {second}."),
    # The event's own name is NOT here: it is the conference's official title
    # and inventing translations of it is not this file's business. Only the
    # month, which is a date rather than a name.
    ("brand.dates", "Díli, 2–3 October 2026",
     "Díli, 2–3 de outubro de 2026", "Díli, 2–3 Outubru 2026"),

    # ---- settings ----
    ("settings.title", "Settings", "Configurações", "Konfigurasaun"),
    ("settings.subtitle", "This server, and how this dashboard looks",
     "Este servidor, e o aspeto deste painel",
     "Servidor ida ne’e, no oinsa painel ne’e hatudu"),

    ("settings.server", "Server and connection", "Servidor e ligação",
     "Servidor no ligasaun"),
    ("settings.serverNote",
     "What the server says about itself. Point every phone and screen at the address below.",
     "O que o servidor diz sobre si. Aponte cada telemóvel e ecrã para o endereço abaixo.",
     "Saida servidor dehan kona-ba nia an. Hatudu telefone no ekrán hotu ba enderesu iha kraik."),
    ("settings.lanAddress", "LAN address", "Endereço na rede", "Enderesu iha rede"),
    ("settings.lanAddressNote", "Devices reach the server here",
     "Os dispositivos chegam ao servidor aqui",
     "Aparelhu sira liga ba servidor iha ne’e"),
    ("settings.copy", "Copy", "Copiar", "Kopia"),
    ("settings.copied", "Copied", "Copiado", "Kopia ona"),
    ("settings.reachable", "Reachable", "Acessível", "Bele hetan"),
    ("settings.reachableYes", "Answered in {ms} ms", "Respondeu em {ms} ms",
     "Responde iha {ms} ms"),
    ("settings.reachableNo", "No answer", "Sem resposta", "La responde"),
    ("settings.unreachableBody",
     "The dashboard reached its own server but not the backend. Check that uvicorn is running.",
     "O painel alcançou o seu próprio servidor mas não o backend. Verifique se o uvicorn está a correr.",
     "Painel liga ba nia servidor rasik maibe la liga ba backend. Haree se uvicorn la’o hela."),
    ("settings.service", "Service", "Serviço", "Servisu"),
    ("settings.serverClock", "Server clock", "Relógio do servidor",
     "Relójiu servidor"),
    ("settings.browserClock", "This browser", "Este navegador", "Navegador ne’e"),
    ("settings.drift", "Clock difference", "Diferença de relógio",
     "Diferensa relójiu"),
    ("settings.driftAhead", "{amount} ahead", "{amount} à frente",
     "{amount} avansa"),
    ("settings.driftBehind", "{amount} behind", "{amount} atrasado",
     "{amount} atrasu"),
    ("settings.driftLevel", "In step", "Em sincronia", "Hanesan"),
    ("settings.driftNote",
     "A guard’s phone stamps its own scan time, and the report groups those by hour. Clocks more than a minute apart can file an arrival in the wrong one.",
     "O telemóvel do guarda marca a sua própria hora de leitura, e o relatório agrupa-as por hora. Relógios com mais de um minuto de diferença podem colocar uma chegada na hora errada.",
     "Telefone guarda nian marka nia oras leitura rasik, no relatóriu grupu sira tuir oras. Relójiu ne’ebe diferensa liu minutu ida bele tau xegada iha oras sala."),
    ("settings.checkedAt", "Checked at {time}", "Verificado às {time}",
     "Verifika iha {time}"),
    ("settings.checkAgain", "Check again", "Verificar de novo", "Verifika fali"),
    ("settings.checking", "Checking…", "A verificar…", "Verifika hela…"),

    ("settings.appearance", "Appearance", "Aparência", "Hahalok"),
    ("settings.appearanceNote",
     "Kept in this browser. Every desk can choose its own.",
     "Guardado neste navegador. Cada posto pode escolher o seu.",
     "Rai iha navegador ne’e. Meza ida-idak bele hili nian."),
    ("settings.themeLabel", "Theme", "Tema", "Tema"),
    ("settings.languageLabel", "Language", "Idioma", "Lian"),

    ("//assistant", "", "", ""),
    ("assistant.launcher", "Ask", "Perguntar", "Husu"),
    ("assistant.title", "Ask about the event", "Perguntar sobre o evento",
     "Husu kona-ba eventu"),
    ("assistant.subtitle",
     "Answers come from the registration and entrance records.",
     "As respostas vêm dos registos de inscrição e de entrada.",
     "Resposta mai husi rejistu inskrisaun no tama nian."),
    ("assistant.close", "Close", "Fechar", "Taka"),
    ("assistant.clear", "New conversation", "Nova conversa", "Konversa foun"),
    ("assistant.emptyLead",
     "Ask in your own words, or start with one of these.",
     "Pergunte por palavras suas, ou comece por uma destas.",
     "Husu ho ita-nia liafuan rasik, ka hahú ho ida husi ne’e."),
    ("assistant.suggest.dayOne", "How many people arrived on 2 October?",
     "Quantas pessoas chegaram a 2 de outubro?",
     "Ema na’in hira mak to’o iha loron 2 Outubru?"),
    ("assistant.suggest.vipAbsent", "Which VIP guests never arrived?",
     "Que convidados VIP nunca chegaram?",
     "Konvidadu VIP sira ne’ebé mak la to’o?"),
    ("assistant.suggest.refused", "Who was refused at the door, and when?",
     "Quem foi recusado à entrada, e quando?",
     "Se mak hetan rejeisaun iha odamatan, no bainhira?"),
    ("assistant.suggest.excel",
     "Give me the entrance report for both days as Excel",
     "Dê-me o relatório de entradas dos dois dias em Excel",
     "Fó relatóriu tama ba loron rua nian iha Excel"),
    ("assistant.placeholder", "Ask about arrivals, visitors or refusals",
     "Pergunte sobre chegadas, visitantes ou recusas",
     "Husu kona-ba xegada, vizitante ka rejeisaun"),
    ("assistant.send", "Send", "Enviar", "Haruka"),
    ("assistant.inputHint", "Enter to send, Shift+Enter for a new line",
     "Enter para enviar, Shift+Enter para nova linha",
     "Enter atu haruka, Shift+Enter ba liña foun"),
    ("assistant.thinking", "Reading the records…", "A ler os registos…",
     "Lee hela rejistu…"),
    ("assistant.you", "You", "Você", "Ita"),
    ("assistant.bot", "Assistant", "Assistente", "Asistente"),
    ("assistant.privacy",
     "Answers are written by OpenAI from this event’s records. Photos and badge codes are never sent.",
     "As respostas são escritas pela OpenAI a partir dos registos deste evento. Fotografias e códigos de crachá nunca são enviados.",
     "OpenAI mak hakerek resposta husi rejistu eventu ne’e nian. Foto no kódigu kartaun nunka haruka."),
    ("assistant.disabled",
     "The assistant is switched off on this server. Add OPENAI_API_KEY to vms-backend/.env and restart the backend.",
     "O assistente está desligado neste servidor. Adicione OPENAI_API_KEY a vms-backend/.env e reinicie o backend.",
     "Asistente mate iha servidor ne’e. Aumenta OPENAI_API_KEY ba vms-backend/.env no reinisia backend."),
    ("assistant.retry", "Try again", "Tentar de novo", "Koko fali"),
    ("assistant.error.throttled",
     "Too many questions in a minute. Wait a moment and try again.",
     "Demasiadas perguntas num minuto. Aguarde um momento e tente de novo.",
     "Pergunta barak liu iha minutu ida. Hein uitoan no koko fali."),
    ("assistant.error.network",
     "The backend did not answer. Check that it is running.",
     "O backend não respondeu. Verifique se está a correr.",
     "Backend la responde. Haree se nia la’o hela."),
    ("assistant.error.stale",
     "The backend does not have the assistant yet. Restart it to load the new code.",
     "O backend ainda não tem o assistente. Reinicie-o para carregar o código novo.",
     "Backend seidauk iha asistente. Reinisia nia atu karrega kódigu foun."),
    ("assistant.error.unexpected", "The question could not be answered.",
     "Não foi possível responder à pergunta.",
     "La konsege responde pergunta ne’e."),
    ("assistant.download", "Download", "Descarregar", "Deskarega"),
    ("assistant.downloading", "Preparing…", "A preparar…", "Prepara hela…"),
    ("assistant.downloadFailed", "The file could not be downloaded.",
     "Não foi possível descarregar o ficheiro.",
     "La konsege deskarega arkivu."),
    ("assistant.file.entrance", "Entrance report", "Relatório de entradas",
     "Relatóriu tama"),
    ("assistant.file.visitors", "Visitor list with QR codes",
     "Lista de visitantes com códigos QR", "Lista vizitante ho kódigu QR"),
    ("assistant.file.allVisitors", "Every registered visitor",
     "Todos os visitantes inscritos", "Vizitante rejistadu hotu"),
    ("assistant.file.oneDay", "{day}", "{day}", "{day}"),
    ("assistant.file.range", "{from} to {to}", "{from} a {to}",
     "{from} to’o {to}"),
]


def literal(text):
    out = []
    for ch in text:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ord(ch) < 128:
            out.append(ch)
        else:
            out.append("\\u%04x" % ord(ch))
    return '"' + "".join(out) + '"'


def build(head, tail, index):
    lines = [head]
    for entry in M:
        key = entry[0]
        if key.startswith("//"):
            name = key[2:]
            lines.append("")
            lines.append("  // " + "-" * (68 - len(name)) + " " + name + " --")
            continue
        value = literal(entry[index])
        one = '  "%s": %s,' % (key, value)
        if len(one) <= 80:
            lines.append(one)
        else:
            lines.append('  "%s":' % key)
            lines.append("    %s," % value)
    lines.append(tail)
    return "\n".join(lines)


ROOT.joinpath("en.ts").write_text(build(HEAD_EN, TAIL_EN, 1), encoding="utf-8")
ROOT.joinpath("pt.ts").write_text(build(HEAD_PT, "};\n", 2), encoding="utf-8")
ROOT.joinpath("tet.ts").write_text(build(HEAD_TET, "};\n", 3), encoding="utf-8")

for name in ("en.ts", "pt.ts", "tet.ts"):
    raw = ROOT.joinpath(name).read_bytes()
    bad = [b for b in raw if b > 127]
    keys = sum(1 for e in M if not e[0].startswith("//"))
    print("%-6s bytes=%-6d non-ascii=%-3d keys=%d" % (name, len(raw), len(bad), keys))
