import type { Messages } from "./en";

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
export const pt: Messages = {

  // --------------------------------------------------------------- shell --
  "nav.sections": "Sec\u00e7\u00f5es",
  "nav.group.overview": "Vis\u00e3o geral",
  "nav.group.accreditation": "Acredita\u00e7\u00e3o",
  "nav.group.operations": "Opera\u00e7\u00f5es",
  "nav.dashboard": "Painel",
  "nav.dashboard.hint": "Chegadas e estado das portas",
  "nav.visitors": "Visitantes",
  "nav.visitors.hint": "Registar e emitir crach\u00e1s",
  "nav.badges": "Crach\u00e1s",
  "nav.badges.hint": "Fila de impress\u00e3o",
  "nav.devices": "Dispositivos",
  "nav.devices.hint": "Portas e ecr\u00e3s",
  "nav.reports": "Relat\u00f3rios",
  "nav.reports.hint": "Registo de entradas",
  "nav.expand": "Expandir menu",
  "nav.collapse": "Recolher menu",
  "nav.signOut": "Terminar sess\u00e3o",
  "nav.signingOut": "A terminar sess\u00e3o\u2026",
  "nav.settings": "Configura\u00e7\u00f5es",
  "nav.settings.hint": "Servidor e apar\u00eancia",
  "nav.silentDevices": "{count} dispositivo sem comunicar recentemente",
  "shell.restoringSession": "A restaurar sess\u00e3o",
  "topbar.localTime": "Hora local",

  // --------------------------------------------------------- preferences --
  "theme.toDark": "Mudar para modo escuro",
  "theme.toLight": "Mudar para modo claro",
  "theme.dark": "Escuro",
  "theme.light": "Claro",
  "language.label": "Idioma",
  "language.choose": "Escolher idioma",

  // --------------------------------------------------------------- login --
  "login.title": "Iniciar sess\u00e3o",
  "login.intro":
    "Apenas contas de administrador. Os seguran\u00e7as usam um telem\u00f3vel emparelhado e o ecr\u00e3 do \u00e1trio emparelha-se sozinho.",
  "login.username": "Utilizador",
  "login.password": "Palavra-passe",
  "login.submit": "Iniciar sess\u00e3o",
  "login.submitting": "A iniciar sess\u00e3o\u2026",
  "login.badCredentials": "O utilizador e a palavra-passe n\u00e3o coincidem.",
  "login.failedStatus": "Falha ao iniciar sess\u00e3o (HTTP {status}).",
  "login.unreachable":
    "N\u00e3o foi poss\u00edvel contactar o servidor. Verifique se o backend est\u00e1 a correr.",
  "login.servingFrom": "A partir de",
  "login.pitch":
    "Registe um visitante, imprima o crach\u00e1 e veja todas as chegadas num s\u00f3 lugar \u2014 na sua pr\u00f3pria rede, sem nada sair do edif\u00edcio.",

  // -------------------------------------------------------------- errors --
  "error.unexpected": "Ocorreu um erro.",
  "error.fields": "H\u00e1 campos por corrigir.",
  "error.visitorLoad": "N\u00e3o foi poss\u00edvel carregar este visitante.",
  "error.visitorRegister": "N\u00e3o foi poss\u00edvel registar o visitante.",
  "error.visitorSave":
    "N\u00e3o foi poss\u00edvel guardar as altera\u00e7\u00f5es.",
  "error.visitorActivate": "N\u00e3o foi poss\u00edvel ativar o visitante.",
  "error.visitorDeactivate":
    "N\u00e3o foi poss\u00edvel desativar o visitante.",
  "error.visitorDelete": "N\u00e3o foi poss\u00edvel eliminar o visitante.",

  // -------------------------------------------------------- visitor list --
  "visitors.title": "Visitantes",
  "visitors.subtitle": "Todos os inscritos no evento",
  "visitors.search": "Procurar visitantes",
  "visitors.searchPlaceholder":
    "Nome, organiza\u00e7\u00e3o, pa\u00eds ou n\u00famero do crach\u00e1",
  "visitors.filterCategory": "Filtrar por categoria",
  "visitors.tab.all": "Todos",
  "visitors.tab.normal": "Normal",
  "visitors.tab.vip": "VIP",
  "visitors.exportTitle":
    "Todos os inscritos, com foto e QR do cart\u00e3o. Nada \u00e9 reemitido.",
  "visitors.exporting": "A exportar\u2026",
  "visitors.export": "Exportar Excel",
  "visitors.exportFailed": "N\u00e3o foi poss\u00edvel exportar a lista.",
  "visitors.register": "Registar visitante",
  "visitors.refreshing": "A atualizar\u2026",
  "visitors.loadFailed": "N\u00e3o foi poss\u00edvel carregar os visitantes",
  "visitors.requestFailed": "O pedido falhou antes de chegar ao servidor.",
  "visitors.serverRejected": "O servidor rejeitou o pedido.",
  "visitors.noneMatch": "Ningu\u00e9m corresponde a esses filtros",
  "visitors.noneMatchBody":
    "Tente uma pesquisa mais curta ou alargue a categoria.",
  "visitors.empty": "Ainda n\u00e3o h\u00e1 visitantes",
  "visitors.emptyBody":
    "Registe o primeiro visitante para emitir um crach\u00e1.",
  "visitors.menu.edit": "Editar dados",
  "visitors.menu.deactivate": "Desativar visitante",
  "visitors.menu.activate": "Ativar visitante",
  "visitors.menu.delete": "Eliminar definitivamente",
  "visitors.status.deactivated": "Desativado",

  // --------------------------------------------------- deactivate dialog --
  "deactivate.title": "Desativar {name}?",
  "deactivate.body":
    "O crach\u00e1 {serial} deixa de funcionar de imediato. A pr\u00f3xima leitura mostra vermelho \u00e0 porta.",
  "deactivate.point1":
    "Continuam na lista de visitantes, marcados como desativados.",
  "deactivate.point2": "O hist\u00f3rico de leituras \u00e9 mantido.",
  "deactivate.point3":
    "Revers\u00edvel. Ativar p\u00f5e o mesmo cart\u00e3o impresso a funcionar \u2014 n\u00e3o h\u00e1 nada para reimprimir.",
  "deactivate.cancel": "Manter ativo",
  "deactivate.confirm": "Desativar",
  "deactivate.pending": "A desativar\u2026",

  // -------------------------------------------------------- purge dialog --
  "purge.warning": "N\u00e3o pode ser anulado",
  "purge.title": "Eliminar {name} definitivamente?",
  "purge.body":
    "Isto remove o registo e a fotografia do visitante do servidor. Desativar \u00e9 a op\u00e7\u00e3o revers\u00edvel; esta n\u00e3o \u00e9.",
  "purge.scansUnknown":
    "As leituras deste crach\u00e1 permanecem no registo de entradas, mas deixam de identificar algu\u00e9m.",
  "purge.scansNone":
    "Nenhuma leitura \u00e9 afetada \u2014 este crach\u00e1 nunca foi apresentado.",
  "purge.scansOne":
    "{count} leitura permanece no registo de entradas, mas deixa de identificar algu\u00e9m.",
  "purge.scansMany":
    "{count} leituras permanecem no registo de entradas, mas deixam de identificar algu\u00e9m.",
  "purge.serialRetired":
    "O crach\u00e1 {serial} \u00e9 retirado. O n\u00famero n\u00e3o \u00e9 reutilizado.",
  "purge.reRegister":
    "Voltar a regist\u00e1-los cria um novo visitante, um novo n\u00famero e um novo QR.",
  "purge.typeToConfirm": "Escreva {serial} para confirmar",
  "purge.cancel": "Cancelar",
  "purge.confirm": "Eliminar definitivamente",
  "purge.pending": "A eliminar\u2026",

  // ------------------------------------------------------ visitor detail --
  "common.loading": "A carregar\u2026",
  "visitor.fallbackTitle": "Visitante",
  "visitor.notFound": "N\u00e3o foi poss\u00edvel carregar este visitante",
  "visitor.notFoundBody":
    "Pode ter sido eliminado. Consulte a lista de visitantes.",
  "visitor.backToAll": "Voltar a todos os visitantes",
  "visitor.allVisitors": "Todos os visitantes",
  "visitor.status.active": "Ativo",
  "visitor.headingActive": "Este crach\u00e1 abre a porta",
  "visitor.headingOff": "Este crach\u00e1 est\u00e1 desligado",
  "visitor.subActive":
    "Qualquer leitor emparelhado aceita-o e o ecr\u00e3 do \u00e1trio d\u00e1 as boas-vindas.",
  "visitor.subOff":
    "A pr\u00f3xima leitura mostra vermelho. Ativar p\u00f5e o mesmo cart\u00e3o a funcionar \u2014 n\u00e3o \u00e9 preciso reimprimir.",
  "visitor.registered": "Registado",
  "visitor.arrivals": "Chegadas",
  "visitor.lastArrival": "\u00daltima chegada",
  "visitor.notYet": "Ainda n\u00e3o",
  "visitor.scansLogged": "Leituras registadas",
  "visitor.activating": "A ativar\u2026",
  "visitor.qrNote":
    "Este QR foi gerado no registo do visitante e nunca muda. Reimprima o cart\u00e3o as vezes que precisar \u2014 l\u00ea-se sempre igual. Desativar para-o e ativar volta a p\u00f4-lo a funcionar, sem tocar no c\u00f3digo do cart\u00e3o. Eliminar definitivamente \u00e9 a \u00fanica coisa aqui que n\u00e3o pode ser anulada.",
  "visitor.scanHistory": "Hist\u00f3rico de leituras",
  "visitor.scanHistoryBody":
    "Todas as vezes que este crach\u00e1 foi apresentado, incluindo as recusadas.",
  "visitor.noScans": "Este crach\u00e1 ainda n\u00e3o foi lido.",
  "visitor.col.event": "Evento",
  "visitor.col.scannedAt": "Lido em",
  "visitor.col.result": "Resultado",
  "visitor.col.device": "Dispositivo",
  "scan.valid": "V\u00e1lido",
  "scan.duplicate": "Duplicado",
  "scan.revoked": "Revogado",
  "scan.invalid": "Inv\u00e1lido",

  // --------------------------------------------------- registration form --
  "register.title": "Registar um visitante",
  "register.subtitle":
    "Um crach\u00e1, impresso com anteced\u00eancia, v\u00e1lido para todo o evento",
  "register.issuedTitle": "Crach\u00e1 emitido",
  "register.issuedSubtitle":
    "Imprima o cart\u00e3o agora, ou mais tarde a partir da p\u00e1gina do visitante",
  "form.photoRequired":
    "Um crach\u00e1 precisa de uma fotografia. Adicione uma antes de registar.",
  "form.fullName": "Nome completo",
  "form.fullNameHint": "Como deve aparecer no crach\u00e1.",
  "form.country": "Pa\u00eds",
  "form.organisation": "Organiza\u00e7\u00e3o",
  "form.optional": "Opcional.",
  "form.category": "Categoria",
  "form.cat.normal": "Normal",
  "form.cat.normalNote": "Crach\u00e1 normal",
  "form.cat.vip": "VIP",
  "form.cat.vipNote": "Cart\u00e3o distinto e boas-vindas no \u00e1trio",
  "form.registering": "A registar\u2026",
  "form.saving": "A guardar\u2026",
  "form.register": "Registar e emitir crach\u00e1",
  "form.save": "Guardar altera\u00e7\u00f5es",
  "form.noteCreate":
    "O n\u00famero \u00e9 atribu\u00eddo no momento do registo. O QR \u00e9 gerado nesse mesmo instante e nunca muda depois.",
  "form.noteEdit":
    "Editar os dados n\u00e3o reemite o crach\u00e1. O n\u00famero e o c\u00f3digo QR ficam exatamente como foram impressos.",

  // ------------------------------------------------------- badge receipt --
  "receipt.badgeIssued": "Crach\u00e1 emitido",
  "receipt.registered": "{name} est\u00e1 registado",
  "receipt.permanent":
    "Este QR \u00e9 permanente. Foi gerado quando {name} foi registado e n\u00e3o muda \u2014 imprima-o agora, ou mais tarde a partir da p\u00e1gina do visitante, as vezes que precisar. S\u00f3 deixa de funcionar se desativar ou eliminar o visitante.",
  "receipt.qrAlt": "C\u00f3digo QR do crach\u00e1 {serial}",
  "receipt.badgeToken": "Token do crach\u00e1",
  "receipt.rendering": "A gerar\u2026",
  "receipt.downloadPdf": "Transferir PDF do crach\u00e1",
  "receipt.print": "Imprimir crach\u00e1",
  "receipt.printFellBack":
    "Os pop-ups est\u00e3o bloqueados para este site, por isso o crach\u00e1 foi transferido. Abra o ficheiro e imprima a partir da\u00ed.",
  "receipt.copied": "Copiado",
  "receipt.copyToken": "Copiar token",
  "receipt.qrFailed":
    "N\u00e3o foi poss\u00edvel desenhar o c\u00f3digo QR. Copie o token e imprima o crach\u00e1 noutra m\u00e1quina, em vez de emitir um cart\u00e3o sem c\u00f3digo.",
  "receipt.copiedAnnounce":
    "Token do crach\u00e1 copiado para a \u00e1rea de transfer\u00eancia.",
  "receipt.badgeSerial": "N\u00famero do crach\u00e1",
  "receipt.registerAnother": "Registar outro visitante",
  "receipt.open": "Abrir {name}",
  "receipt.renderFailed": "N\u00e3o foi poss\u00edvel gerar o crach\u00e1.",

  // ---------------------------------------------------------------- edit --
  "edit.title": "Editar {name}",
  "edit.fallbackTitle": "Editar visitante",

  // ----------------------------------------------- photo upload and crop --
  "photo.label": "Fotografia",
  "photo.spec": "3:4 VERTICAL \u00b7 600 \u00d7 800",
  "photo.notImage": "Isso n\u00e3o \u00e9 uma imagem. Escolha um JPEG ou PNG.",
  "photo.tooLarge": "Essa imagem tem mais de 20 MB. Escolha uma mais pequena.",
  "photo.alt": "A fotografia do crach\u00e1 do visitante",
  "photo.ready": "Recortada e pronta.",
  "photo.onFile":
    "A fotografia j\u00e1 guardada. Mant\u00e9m-se a menos que a substitua.",
  "photo.adjustCrop": "Ajustar recorte",
  "photo.chooseDifferent": "Escolher outra fotografia",
  "photo.add": "Adicionar fotografia",
  "photo.dropHint":
    "Largue uma aqui, ou clique para escolher. A seguir recorta-a.",
  "photo.dialogLabel": "Recortar a fotografia do visitante",
  "photo.frameFace": "Enquadrar o rosto",
  "photo.closeWithoutSaving": "Fechar sem guardar",
  "crop.alt": "A fotografia a ser recortada",
  "crop.preview": "Imagem recortada",
  "crop.circleHint":
    "S\u00f3 o c\u00edrculo \u00e9 impresso e mostrado no ecr\u00e3 do \u00e1trio. Preencha-o com a cabe\u00e7a e os ombros.",
  "crop.aspect": "Propor\u00e7\u00e3o",
  "crop.ratio.badge": "Crach\u00e1 (fixo)",
  "crop.ratio.square": "Quadrado",
  "crop.ratio.free": "Livre",
  "crop.width": "Largura",
  "crop.height": "Altura",
  "crop.heightLocked": "Altura (fixa)",
  "crop.tooSmall":
    "Este recorte tem {width}px de largura. O crach\u00e1 imprime a fotografia a {min}px para 300dpi, por isso ficar\u00e1 desfocada no cart\u00e3o. Recorte menos, ou use uma fotografia maior.",
  "crop.quality": "Qualidade da imagem",
  "crop.bestCompression": "Mais compress\u00e3o",
  "crop.bestQuality": "Mais qualidade",
  "crop.applying": "A aplicar\u2026",
  "crop.use": "Usar esta fotografia",
  "crop.changeImage": "Mudar de imagem",

  // -------------------------------------------------------------- badges --
  "badges.title": "Impress\u00e3o de crach\u00e1s",
  "badges.subtitle": "Nove por folha A4, com marcas de corte",
  "badges.loadFailed":
    "N\u00e3o foi poss\u00edvel carregar a lista de visitantes.",
  "badges.safeTitle": "Imprimir de novo \u00e9 seguro",
  "badges.safeBody":
    "Cada folha leva o QR j\u00e1 existente de cada visitante, por isso um cart\u00e3o pode ser reimpresso as vezes que precisar e os j\u00e1 entregues continuam a funcionar. Para travar um cart\u00e3o perdido, desative esse visitante na p\u00e1gina dele \u2014 o QR nunca muda, por isso ativ\u00e1-lo de novo p\u00f5e o mesmo cart\u00e3o a funcionar.",
  "badges.searchPlaceholder":
    "Nome, organiza\u00e7\u00e3o, pa\u00eds ou n\u00famero",
  "badges.clearSelection": "Limpar sele\u00e7\u00e3o",
  "badges.selectAll": "Selecionar todos ({count})",
  "badges.print": "Imprimir",
  "badges.printCount": "Imprimir {count}",
  "badges.sheetFailed": "N\u00e3o foi poss\u00edvel produzir a folha.",
  "badges.export": "Exportar Excel",
  "badges.fileFailed": "N\u00e3o foi poss\u00edvel produzir o ficheiro.",
  "badges.selectedOne": "{count} selecionado \u00b7 {sheets} folha A4",
  "badges.selectedMany": "{count} selecionados \u00b7 {sheets} folhas A4",
  "badges.noMatch": "Nenhum visitante corresponde a essa pesquisa.",
  "badges.onSheet": "Na folha",
  "badges.notPrinting": "Fora da folha",
  "badges.menu.selection": "{count} visitantes selecionados",
  "badges.menu.printOne": "Imprimir crach\u00e1",
  "badges.menu.printMany": "Imprimir {count} crach\u00e1s",
  "badges.menu.exportOne": "Exportar para Excel\u2026",
  "badges.menu.exportMany": "Exportar {count} para Excel\u2026",

  // ----------------------------------------------- visitors list: source --
  "visitors.filterSource": "Filtrar por quem registou",
  "visitors.source.all": "Todos",
  "visitors.source.admin": "Balc\u00e3o",
  "visitors.source.self": "Autorregisto",
  "visitors.source.desk": "Balc\u00e3o de registo",
  "visitors.possibleDuplicate": "Poss\u00edvel duplicado",
  "visitors.possibleDuplicateTitle":
    "Outro registo tem o mesmo nome e pa\u00eds.",

  // --------------------------------------- settings: public registration --
  "settings.registration": "Registo p\u00fablico",
  "settings.registrationNote":
    "Permite que os visitantes se registem pelo telem\u00f3vel na rede do evento. Cada um fica registado de imediato com um crach\u00e1 normal.",
  "settings.registrationToggle": "Permitir registo p\u00fablico",
  "settings.registrationOpen": "Aberto",
  "settings.registrationClosed": "Fechado",
  "settings.registrationUrl": "Liga\u00e7\u00e3o de registo",
  "settings.registrationUrlNote":
    "Os telem\u00f3veis t\u00eam de estar no Wi-Fi do evento para a abrir.",
  "settings.registrationNoAddress":
    "O endere\u00e7o de rede do servidor ainda n\u00e3o \u00e9 conhecido.",
  "settings.registrationSaveFailed":
    "N\u00e3o foi poss\u00edvel alterar o interruptor. Tente novamente.",
  "settings.registrationLoadFailed":
    "O servidor n\u00e3o respondeu a esta defini\u00e7\u00e3o. Se foi atualizado agora, tem de ser reiniciado.",
  "settings.registrationSaveQr": "Guardar c\u00f3digo QR",
  "settings.registrationUpdated":
    "Alterado pela \u00faltima vez {time} por {user}",

  // -------------------------------------------- public registration page --
  "publicRegister.title": "Registo no evento",
  "publicRegister.intro":
    "Preencha os seus dados e adicione uma fotografia. Recebe um c\u00f3digo QR para mostrar \u00e0 entrada.",
  "publicRegister.fullName": "Nome completo",
  "publicRegister.country": "Pa\u00eds",
  "publicRegister.countryPlaceholder": "Comece a escrever o seu pa\u00eds",
  "country.listLabel": "Pa\u00edses",
  "country.noMatch": "Nenhum pa\u00eds corresponde a \u201c{text}\u201d",
  "country.invalid": "Selecione o seu pa\u00eds da lista.",
  "publicRegister.organization": "Organiza\u00e7\u00e3o (opcional)",
  "publicRegister.photo": "A sua fotografia",
  "publicRegister.photoHint":
    "Olhe para a c\u00e2mara com boa luz, sem mais ningu\u00e9m na imagem.",
  "publicRegister.choosePhoto": "Tirar ou escolher fotografia",
  "publicRegister.useCamera": "Usar a c\u00e2mara",
  "publicRegister.capture": "Tirar fotografia",
  "publicRegister.cancel": "Cancelar",
  "publicRegister.cameraFailed":
    "N\u00e3o foi poss\u00edvel abrir a c\u00e2mara.",
  "publicRegister.changePhoto": "Mudar fotografia",
  "publicRegister.reviewPhoto": "Recorte a sua fotografia",
  "publicRegister.usePhoto": "Usar esta fotografia",
  "publicRegister.retakePhoto": "Tirar a fotografia novamente",
  "publicRegister.cropTooSmall":
    "Demasiado pequena para imprimir. Arraste os cantos para fora.",
  "publicRegister.checkingFace": "A verificar a fotografia\u2026",
  "publicRegister.faceNone":
    "Nenhum rosto encontrado. Olhe para a c\u00e2mara com boa luz e tente novamente.",
  "publicRegister.faceMany":
    "Foi encontrado mais de um rosto. S\u00f3 deve estar voc\u00ea na fotografia.",
  "publicRegister.faceOk": "A fotografia est\u00e1 boa.",
  "publicRegister.consent":
    "A sua fotografia e os seus dados s\u00e3o usados para o acesso ao evento e apagados depois do evento.",
  "publicRegister.submit": "Registar",
  "publicRegister.submitting": "A registar\u2026",
  "publicRegister.loading": "A carregar\u2026",
  "publicRegister.closedTitle": "O registo est\u00e1 fechado",
  "publicRegister.closedBody": "Dirija-se ao balc\u00e3o de registo.",
  "publicRegister.unreachable":
    "N\u00e3o \u00e9 poss\u00edvel contactar o servidor do evento. Confirme que est\u00e1 no Wi-Fi do evento.",
  "publicRegister.unavailableTitle":
    "O registo n\u00e3o est\u00e1 dispon\u00edvel neste momento",
  "publicRegister.failed":
    "O registo falhou. Tente novamente ou dirija-se ao balc\u00e3o de registo.",
  "publicRegister.tooMany":
    "Demasiados registos a partir desta liga\u00e7\u00e3o. Dirija-se ao balc\u00e3o de registo.",
  "publicRegister.tooLarge":
    "A fotografia \u00e9 demasiado grande. Escolha outra.",
  "publicRegister.successTitle": "Est\u00e1 registado",
  "publicRegister.successShow": "Mostre este c\u00f3digo QR \u00e0 entrada.",
  "publicRegister.brightness":
    "Aumente o brilho do ecr\u00e3 antes de ler o c\u00f3digo.",
  "publicRegister.deskHelp":
    "Se a leitura falhar, dirija-se ao balc\u00e3o e indique {serial}.",
  "publicRegister.keepPage":
    "Mantenha esta p\u00e1gina aberta at\u00e9 entrar.",
  "publicRegister.qrAlt": "C\u00f3digo QR do crach\u00e1 {serial}",
  "publicRegister.saveTitle": "Guarde no seu telem\u00f3vel",
  "publicRegister.saveBody":
    "Guarde o c\u00f3digo para o ter mesmo que esta p\u00e1gina feche.",
  "publicRegister.saveQr": "Guardar c\u00f3digo QR",
  "publicRegister.savingQr": "A preparar\u2026",
  "publicRegister.saveDone": "Guardado no seu telem\u00f3vel.",
  "publicRegister.saveOpened":
    "Toque sem soltar na imagem e escolha Guardar imagem.",
  "publicRegister.saveFailed":
    "N\u00e3o foi poss\u00edvel guardar. Fa\u00e7a uma captura de ecr\u00e3 desta p\u00e1gina.",
  "publicRegister.closedNow":
    "O registo acabou de fechar. V\u00e1 ao balc\u00e3o de registo para terminar.",
  "publicRegister.takePhoto": "Tirar fotografia",
  "publicRegister.chooseFromGallery": "Escolher da galeria",

  // ------------------------------------------------------- export dialog --
  "export.titleOne":
    "Exportar c\u00f3digos de crach\u00e1 de {count} visitante?",
  "export.titleMany":
    "Exportar c\u00f3digos de crach\u00e1 de {count} visitantes?",
  "export.body":
    "Este ficheiro cont\u00e9m um {strong} para cada visitante nele. Exportar n\u00e3o altera nada \u2014 os c\u00f3digos s\u00e3o os que j\u00e1 est\u00e3o nos cart\u00f5es \u2014 mas quem tiver o ficheiro consegue produzir um crach\u00e1 que \u00e9 lido.",
  "export.bodyStrong": "c\u00f3digo QR funcional",
  "export.point1":
    "Envie-o como enviaria os cart\u00f5es impressos, n\u00e3o como enviaria uma lista de convidados.",
  "export.point2":
    "Exportar de novo mais tarde produz um ficheiro id\u00eantico. Perder este s\u00f3 custa o tempo de o exportar outra vez.",
  "export.point3":
    "Para travar um crach\u00e1 espec\u00edfico, desative esse visitante na p\u00e1gina dele. Apagar o ficheiro n\u00e3o trava nada.",
  "export.building": "A preparar\u2026",
  "export.confirm": "Exportar e transferir",
  "card.deactivated": "Desativado",
  "card.qrOnCard": "no cart\u00e3o impresso",
  "card.qrDrawing": "a desenhar\u2026",
  "card.qrFailed": "n\u00e3o foi poss\u00edvel desenhar",

  // ------------------------------------------------------------- devices --
  "time.justNow": "agora mesmo",
  "device.kind.scanner": "Leitor",
  "device.kind.screen": "Ecr\u00e3",
  "device.kind.desk": "Balc\u00e3o",
  "device.kindInline.scanner": "leitor",
  "device.kindInline.screen": "ecr\u00e3",
  "device.kindInline.desk": "balc\u00e3o",
  "devices.subtitleQuiet":
    "Telem\u00f3veis dos seguran\u00e7as e o ecr\u00e3 do \u00e1trio",
  "devices.silentOne":
    "{count} dispositivo n\u00e3o comunica h\u00e1 algum tempo",
  "devices.silentMany":
    "{count} dispositivos n\u00e3o comunicam h\u00e1 algum tempo",
  "devices.alertOne": "{count} dispositivo est\u00e1 em sil\u00eancio.",
  "devices.alertMany": "{count} dispositivos est\u00e3o em sil\u00eancio.",
  "devices.alertBody":
    "Uma porta sem leituras h\u00e1 dez minutos ou est\u00e1 parada ou est\u00e1 offline \u2014 v\u00e1 l\u00e1 verificar.",
  "devices.paired": "Dispositivos emparelhados",
  "devices.pairedBody":
    "Atualiza sozinho. \u201cVisto pela \u00faltima vez\u201d \u00e9 o \u00faltimo pedido feito pelo dispositivo, e \u00e9 assim que se distingue uma porta parada de um telem\u00f3vel morto.",
  "devices.loadFailed": "N\u00e3o foi poss\u00edvel carregar os dispositivos",
  "devices.none": "Ainda n\u00e3o h\u00e1 dispositivos emparelhados",
  "devices.noneBody":
    "Gere um c\u00f3digo acima e introduza-o no telem\u00f3vel do seguran\u00e7a ou no ecr\u00e3 do \u00e1trio.",
  "devices.col.device": "Dispositivo",
  "devices.col.kind": "Tipo",
  "devices.col.lastSeen": "Visto pela \u00faltima vez",
  "devices.col.state": "Estado",
  "devices.neverCheckedIn": "Nunca comunicou",
  "devices.silentCheck": "Em sil\u00eancio \u2014 verifique a porta",
  "devices.notSeenSincePairing": "Sem sinal desde o emparelhamento",
  "devices.stateRevoked": "REVOGADO",
  "devices.stateActive": "ATIVO",
  "devices.revoke": "Revogar",

  // ------------------------------------------------------------- pairing --
  "pair.title": "Emparelhar um dispositivo",
  "pair.body":
    "Abra a aplica\u00e7\u00e3o no telem\u00f3vel ou no ecr\u00e3 e leia-lhe o c\u00f3digo abaixo. Cada c\u00f3digo funciona uma s\u00f3 vez.",
  "pair.codeButton": "C\u00f3digo de {kind}",
  "pair.blurb.scanner": "O telem\u00f3vel de um seguran\u00e7a, a uma porta",
  "pair.blurb.screen": "O ecr\u00e3 do \u00e1trio",
  "pair.blurb.desk":
    "Um port\u00e1til ou tablet que regista visitantes \u00e0 porta",
  "pair.deskLink": "Liga\u00e7\u00e3o do balc\u00e3o",
  "pair.deskLinkBody":
    "Abra isto no dispositivo do balc\u00e3o e escreva o c\u00f3digo acima. S\u00f3 \u00e9 mostrado aqui uma vez.",
  "pair.deskLinkWarn":
    "Mantenha a liga\u00e7\u00e3o privada. Quem tiver a liga\u00e7\u00e3o e um c\u00f3digo pode registar visitantes.",
  "pair.deskLinkNoAddress":
    "O endere\u00e7o de rede do servidor ainda n\u00e3o \u00e9 conhecido.",
  "pair.copyLink": "Copiar liga\u00e7\u00e3o",
  "pair.copied": "Copiado",
  "pair.copyManual": "Selecionado \u2014 prima Ctrl+C para copiar.",
  "pair.codeLabel": "C\u00f3digo de emparelhamento de {kind}",
  "pair.expired":
    "Este c\u00f3digo expirou. Gere outro \u2014 n\u00e3o foi emparelhado nada com ele.",
  "pair.expiresIn": "Expira em",
  "desk.title": "Balc\u00e3o de registo",
  "desk.pairTitle": "Emparelhar este balc\u00e3o",
  "desk.pairBody":
    "Escreva o c\u00f3digo do painel. S\u00f3 faz isto uma vez neste dispositivo.",
  "desk.codeLabel": "C\u00f3digo de emparelhamento",
  "desk.nameLabel": "Nome do balc\u00e3o",
  "desk.namePlaceholder": "Entrada principal",
  "desk.nameHint":
    "Onde est\u00e1 este balc\u00e3o. Um administrador v\u00ea-o na lista de dispositivos.",
  "desk.pair": "Emparelhar",
  "desk.pairing": "A emparelhar\u2026",
  "desk.pairFailed": "Esse c\u00f3digo n\u00e3o foi aceite.",
  "desk.formTitle": "Registar um visitante",
  "desk.fullName": "Nome completo",
  "desk.country": "Pa\u00eds",
  "desk.organization": "Organiza\u00e7\u00e3o (opcional)",
  "desk.category": "Tipo de crach\u00e1",
  "desk.normal": "Normal",
  "desk.vip": "VIP",
  "desk.photo": "Fotografia do visitante",
  "desk.photoHint": "Tire a fotografia ou escolha uma deste dispositivo.",
  "desk.register": "Registar visitante",
  "desk.registering": "A registar\u2026",
  "desk.doneTitle": "Registado",
  "desk.showQr": "Pe\u00e7a ao visitante para fotografar este c\u00f3digo.",
  "desk.keepIt": "Mostram-no \u00e0 entrada, hoje ou amanh\u00e3.",
  "desk.again": "Registar outro visitante",
  "desk.downloadQr": "Descarregar c\u00f3digo QR",
  "desk.downloading": "A preparar\u2026",
  "desk.downloadDone": "Guardado. Partilhe com o visitante.",
  "desk.downloadOpened": "Toque sem soltar na imagem e escolha Guardar imagem.",
  "desk.downloadFailed":
    "N\u00e3o foi poss\u00edvel guardar. Pe\u00e7a ao visitante para fotografar o c\u00f3digo.",
  "desk.qrAlt": "C\u00f3digo QR do crach\u00e1 {serial}",
  "desk.qrFailed":
    "N\u00e3o foi poss\u00edvel desenhar o c\u00f3digo. Registe novamente este visitante.",
  "desk.unpaired":
    "Este balc\u00e3o j\u00e1 n\u00e3o est\u00e1 emparelhado. Pe\u00e7a um c\u00f3digo novo a um administrador.",
  "desk.wrongDevice": "Esse c\u00f3digo \u00e9 para outro tipo de dispositivo.",
  "desk.tooMany":
    "Demasiados registos deste balc\u00e3o. Espere alguns minutos.",
  "desk.tooLarge": "A fotografia \u00e9 demasiado grande. Escolha outra.",
  "desk.failed":
    "N\u00e3o foi poss\u00edvel registar o visitante. Tente novamente.",
  "desk.unreachable":
    "N\u00e3o \u00e9 poss\u00edvel contactar o servidor do evento.",
  "pair.alphabetNote":
    "Os c\u00f3digos nunca cont\u00eam 0, O, 1 nem I \u2014 esses quatro ficam de fora porque s\u00e3o os que as pessoas ouvem e escrevem mal. O dispositivo aparece na lista abaixo assim que emparelha.",

  // ------------------------------------------------ revoke device dialog --
  "revokeDevice.title": "Revogar {name}?",
  "revokeDevice.body":
    "Este {kind} deixa de funcionar {strong}. Se for um telem\u00f3vel de porta, essa porta n\u00e3o consegue registar chegadas at\u00e9 algu\u00e9m o emparelhar de novo.",
  "revokeDevice.bodyStrong": "de imediato",
  "revokeDevice.point1":
    "{strong} \u2014 em segundos, sem ningu\u00e9m ter de l\u00e1 ir. Tenha um novo c\u00f3digo de emparelhamento pronto se quiser traz\u00ea-lo logo de volta.",
  "revokeDevice.point1Strong": "Volta sozinho ao ecr\u00e3 de emparelhamento",
  "revokeDevice.point2":
    "O seu token morreu. N\u00e3o h\u00e1 forma de anular \u2014 recuper\u00e1-lo implica um novo c\u00f3digo de emparelhamento.",
  "revokeDevice.point3":
    "As leituras que j\u00e1 registou s\u00e3o mantidas, e as que guardou offline ainda sincronizam quando voltar a emparelhar.",
  "revokeDevice.point4":
    "Permanece nesta lista, marcado como revogado, para o registo de auditoria se manter.",
  "revokeDevice.cancel": "Manter ativo",
  "revokeDevice.pending": "A revogar\u2026",
  "revokeDevice.confirm": "Revogar dispositivo",
  "error.deviceLoad":
    "N\u00e3o foi poss\u00edvel carregar a lista de dispositivos.",
  "error.pairingCode":
    "N\u00e3o foi poss\u00edvel gerar um c\u00f3digo de emparelhamento.",
  "error.deviceRevoke": "N\u00e3o foi poss\u00edvel revogar o dispositivo.",

  // ------------------------------------------------------------- reports --
  "reports.title": "Registo de entradas",
  "reports.subtitleQuiet": "Chegadas e recusas",
  "reports.subtitleRefused": "{count} recusados \u00e0 porta",
  "reports.subtitleNoRefusals": "Nenhum crach\u00e1 recusado neste intervalo",
  "reports.allOutcomes": "Todos os resultados",
  "reports.allCategories": "Todas as categorias",
  "reports.from": "De",
  "reports.to": "At\u00e9",
  "reports.outcome": "Resultado",
  "reports.any": "Qualquer",
  "reports.exportNote":
    "Exatamente como os filtros acima est\u00e3o definidos.",
  "reports.preparing": "A preparar\u2026",
  "reports.exportFailed":
    "N\u00e3o foi poss\u00edvel guardar a exporta\u00e7\u00e3o.",
  "reports.logFailed": "N\u00e3o foi poss\u00edvel carregar o registo",
  "reports.everyBadge": "Todos os crach\u00e1s apresentados",
  "reports.everyBadgeNote":
    "As linhas por tr\u00e1s dos n\u00fameros acima, recusas inclu\u00eddas",
  "reports.timezone": "Horas mostradas em {zone}.",
  "reports.format.pdf": "Relat\u00f3rio PDF",
  "reports.format.pdfHint":
    "O relat\u00f3rio escrito \u2014 conclus\u00f5es, gr\u00e1ficos e tabelas. Para reencaminhar.",
  "reports.format.xlsx": "Livro Excel",
  "reports.format.xlsxHint":
    "Seis folhas, valores como n\u00fameros. Para quem quiser trabalh\u00e1-los.",
  "reports.format.csv": "Registo CSV",
  "reports.format.csvHint":
    "O registo bruto de leituras, uma linha por crach\u00e1 apresentado. Sem an\u00e1lise.",
  "reports.export.stale":
    "Essa exporta\u00e7\u00e3o ainda n\u00e3o existe no servidor \u2014 est\u00e1 a correr uma vers\u00e3o mais antiga do que esta p\u00e1gina. Reinicie o backend e tente de novo.",
  "reports.export.expired":
    "A sua sess\u00e3o expirou. Recarregue a p\u00e1gina e inicie sess\u00e3o de novo.",
  "reports.export.serverError":
    "O servidor n\u00e3o conseguiu produzir essa exporta\u00e7\u00e3o (HTTP {status}).",
  "reports.export.downloadFailed":
    "N\u00e3o foi poss\u00edvel transferir essa exporta\u00e7\u00e3o (HTTP {status}).",
  "error.reportLoad":
    "N\u00e3o foi poss\u00edvel carregar o registo de entradas.",

  // --------------------------------------------------------------- recap --
  "recap.unavailable": "An\u00e1lise indispon\u00edvel",
  "recap.unavailableBody":
    "O servidor respondeu sem as conclus\u00f5es derivadas, o que significa que est\u00e1 a correr uma vers\u00e3o mais antiga do que esta p\u00e1gina. Reinicie o backend e recarregue \u2014 o registo abaixo n\u00e3o \u00e9 afetado e continua exato.",
  "recap.scans": "Leituras",
  "recap.inRange": "Neste intervalo",
  "recap.people": "Pessoas",
  "recap.distinct": "Visitantes distintos",
  "recap.duplicates": "Duplicados",
  "recap.reEntries": "Reentradas, n\u00e3o recusas",
  "recap.refused": "Recusados",
  "recap.invalidOrRevoked": "Inv\u00e1lidos ou revogados",
  "recap.nothingScanned": "Nada lido neste intervalo",
  "recap.nothingScannedBody":
    "Alargue as datas, ou limpe os filtros. Ainda n\u00e3o h\u00e1 nada para relatar.",
  "recap.attendance": "Presen\u00e7a",
  "recap.attendanceNote": "{arrived} de {registered} registados",
  "recap.scansLogged": "Leituras registadas",
  "recap.repeatNote": "{count} pessoas passaram mais do que uma vez",
  "recap.busiestHour": "Hora de maior movimento",
  "recap.peakNote": "{total} leituras \u00b7 {share}% do per\u00edodo",
  "recap.noArrivals": "Nenhuma chegada registada",
  "recap.refusalNote": "{rate}% de tudo o que foi apresentado",
  "recap.noneTurnedAway": "Nenhum crach\u00e1 recusado",
  "recap.whatNumbersSay": "O que dizem os n\u00fameros",
  "recap.whatNumbersSayNote":
    "Gerado a partir deste intervalo \u2014 cada linha \u00e9 uma afirma\u00e7\u00e3o que os dados sustentam",
  "recap.loadByDoor": "Movimento por porta",
  "recap.loadByDoorNote":
    "Uma porta que recusa crach\u00e1s \u00e9 uma porta com um problema",
  "recap.noDoorScan": "Nenhuma porta registou leituras.",
  "recap.refusedHere": "{count} recusados aqui",
  "recap.notArrived": "Registados, ainda n\u00e3o chegaram",
  "recap.notArrivedCount": "{count} de {registered}",
  "recap.notArrivedNote":
    "Sem leitura v\u00e1lida neste intervalo. A lista completa est\u00e1 no PDF e no livro Excel.",
  "recap.andMore": "e mais {count}",

  // ----------------------------------------------------------- entry log --
  "entry.emptyBody": "Alargue as datas, ou limpe os filtros.",
  "entry.col.time": "Hora",
  "entry.col.name": "Nome",
  "chart.noScans":
    "Sem leituras neste intervalo, por isso n\u00e3o h\u00e1 nada para representar.",
  "chart.refused": "Recusados",
  "chart.scansByHour": "Leituras por hora",

  // ------------------------------------------------------------ overview --
  "overview.subtitleQuiet": "As chegadas de hoje em todas as portas",
  "overview.silentOne":
    "{count} porta ficou em sil\u00eancio \u2014 verifique Dispositivos",
  "overview.silentMany":
    "{count} portas ficaram em sil\u00eancio \u2014 verifique Dispositivos",
  "overview.registered": "Registados",
  "overview.vipCount": "{count} VIP",
  "overview.arrivedToday": "Chegaram hoje",
  "overview.arrivedNote": "{percent}% dos registados",
  "overview.refusedAtDoor": "Recusados \u00e0 porta",
  "overview.duplicateOne": "{count} leitura duplicada n\u00e3o contada",
  "overview.duplicateMany": "{count} leituras duplicadas n\u00e3o contadas",
  "overview.doorsReporting": "Portas a comunicar",
  "overview.silentCount": "{count} em sil\u00eancio",
  "overview.allCheckedIn": "Todas comunicaram recentemente",
  "overview.arrivalsByHour": "Chegadas por hora",
  "overview.arrivalsByHourNote":
    "Todos os crach\u00e1s apresentados hoje, marcados na hora em que aconteceu",
  "overview.scanCountOne": "{count} leitura",
  "overview.scanCountMany": "{count} leituras",
  "overview.outcomeSplit": "Divis\u00e3o dos resultados",
  "overview.outcomeSplitNote": "Como se dividiram as leituras de hoje",
  "overview.recentScans": "Leituras recentes",
  "overview.recentScansNote": "Mais recentes primeiro, recusas inclu\u00eddas",
  "overview.nothingToday": "Ainda n\u00e3o foi lido nada hoje.",
  "overview.arrivalsAppear":
    "As chegadas aparecem aqui assim que um seguran\u00e7a l\u00ea um crach\u00e1.",
  "overview.colVisitor": "Visitante",
  "overview.openLog": "Abrir o registo de entradas completo \u2192",
  "overview.arrivedSummary.oneOne":
    "{people} pessoa chegou em {scans} leitura.",
  "overview.arrivedSummary.oneMany":
    "{people} pessoa chegou em {scans} leituras.",
  "overview.arrivedSummary.manyOne":
    "{people} pessoas chegaram em {scans} leitura.",
  "overview.arrivedSummary.manyMany":
    "{people} pessoas chegaram em {scans} leituras.",

  // --------------------------------------------------------------- brand --
  "brand.organisedBy": "Organizado por {first} e {second}.",
  "brand.dates": "D\u00edli, 2\u20133 de outubro de 2026",
  "settings.title": "Configura\u00e7\u00f5es",
  "settings.subtitle": "Este servidor, e o aspeto deste painel",
  "settings.server": "Servidor e liga\u00e7\u00e3o",
  "settings.serverNote":
    "O que o servidor diz sobre si. Aponte cada telem\u00f3vel e ecr\u00e3 para o endere\u00e7o abaixo.",
  "settings.lanAddress": "Endere\u00e7o na rede",
  "settings.lanAddressNote": "Os dispositivos chegam ao servidor aqui",
  "settings.copy": "Copiar",
  "settings.copied": "Copiado",
  "settings.reachable": "Acess\u00edvel",
  "settings.reachableYes": "Respondeu em {ms} ms",
  "settings.reachableNo": "Sem resposta",
  "settings.unreachableBody":
    "O painel alcan\u00e7ou o seu pr\u00f3prio servidor mas n\u00e3o o backend. Verifique se o uvicorn est\u00e1 a correr.",
  "settings.service": "Servi\u00e7o",
  "settings.serverClock": "Rel\u00f3gio do servidor",
  "settings.browserClock": "Este navegador",
  "settings.drift": "Diferen\u00e7a de rel\u00f3gio",
  "settings.driftAhead": "{amount} \u00e0 frente",
  "settings.driftBehind": "{amount} atrasado",
  "settings.driftLevel": "Em sincronia",
  "settings.driftNote":
    "O telem\u00f3vel do guarda marca a sua pr\u00f3pria hora de leitura, e o relat\u00f3rio agrupa-as por hora. Rel\u00f3gios com mais de um minuto de diferen\u00e7a podem colocar uma chegada na hora errada.",
  "settings.checkedAt": "Verificado \u00e0s {time}",
  "settings.checkAgain": "Verificar de novo",
  "settings.checking": "A verificar\u2026",
  "settings.appearance": "Apar\u00eancia",
  "settings.appearanceNote":
    "Guardado neste navegador. Cada posto pode escolher o seu.",
  "settings.themeLabel": "Tema",
  "settings.languageLabel": "Idioma",

  // ----------------------------------------------------------- assistant --
  "assistant.launcher": "Perguntar \u00e0 IA",
  "assistant.launcherLabel": "Perguntar \u00e0 IA sobre o evento",
  "assistant.title": "Assistente de IA",
  "assistant.subtitle":
    "As respostas v\u00eam dos registos de inscri\u00e7\u00e3o e de entrada.",
  "assistant.close": "Fechar",
  "assistant.newConversation": "Nova conversa",
  "assistant.history": "Hist\u00f3rico",
  "assistant.historyTitle": "As suas conversas",
  "assistant.historyEmpty":
    "Ainda n\u00e3o h\u00e1 conversas guardadas. Cada pergunta que fizer fica aqui.",
  "assistant.recent": "Conversas recentes",
  "assistant.recentHint": "Continue onde ficou.",
  "assistant.viewAll": "Ver todas as conversas",
  "assistant.untitled": "Sem t\u00edtulo",
  "assistant.backToChat": "Voltar \u00e0 conversa",
  "assistant.deleteConversation": "Eliminar conversa",
  "assistant.rename": "Mudar o nome",
  "assistant.renameLabel": "Nome da conversa",
  "assistant.renameFailed":
    "N\u00e3o foi poss\u00edvel mudar o nome da conversa.",
  "assistant.cancel": "Cancelar",
  "assistant.moreActions": "Mais a\u00e7\u00f5es",
  "assistant.rowHint":
    "Clique com o bot\u00e3o direito para mudar o nome ou eliminar",
  "assistant.confirmDelete": "Eliminar definitivamente",
  "assistant.loadFailed": "N\u00e3o foi poss\u00edvel carregar a conversa.",
  "assistant.memoriesTitle": "Memorizado",
  "assistant.memoriesHint":
    "Diga \u00ablembra-te\u2026\u00bb numa pergunta para acrescentar uma nota. As notas nunca guardam dados de visitantes.",
  "assistant.memoriesEmpty": "Ainda nada memorizado.",
  "assistant.forget": "Esquecer",
  "assistant.remembered": "Memorizado: {note}",
  "assistant.emptyLead":
    "Pergunte por palavras suas, ou comece por uma destas.",
  "assistant.suggest.dayOne": "Quantas pessoas chegaram a 2 de outubro?",
  "assistant.suggest.vipAbsent": "Que convidados VIP nunca chegaram?",
  "assistant.suggest.refused": "Quem foi recusado \u00e0 entrada, e quando?",
  "assistant.suggest.excel":
    "D\u00ea-me o relat\u00f3rio de entradas dos dois dias em Excel",
  "assistant.placeholder": "Pergunte sobre chegadas, visitantes ou recusas",
  "assistant.send": "Enviar",
  "assistant.inputHint": "Enter para enviar, Shift+Enter para nova linha",
  "assistant.thinking": "A ler os registos\u2026",
  "assistant.you": "Voc\u00ea",
  "assistant.bot": "Assistente",
  "assistant.privacy":
    "As respostas s\u00e3o escritas pela OpenAI a partir dos registos deste evento. Fotografias e c\u00f3digos de crach\u00e1 nunca s\u00e3o enviados.",
  "assistant.disabled":
    "O assistente est\u00e1 desligado neste servidor. Adicione OPENAI_API_KEY a vms-backend/.env e reinicie o backend.",
  "assistant.retry": "Tentar de novo",
  "assistant.error.throttled":
    "Demasiadas perguntas num minuto. Aguarde um momento e tente de novo.",
  "assistant.error.network":
    "O backend n\u00e3o respondeu. Verifique se est\u00e1 a correr.",
  "assistant.error.stale":
    "O backend ainda n\u00e3o tem o assistente. Reinicie-o para carregar o c\u00f3digo novo.",
  "assistant.error.unexpected":
    "N\u00e3o foi poss\u00edvel responder \u00e0 pergunta.",
  "assistant.download": "Descarregar",
  "assistant.downloading": "A preparar\u2026",
  "assistant.downloadFailed":
    "N\u00e3o foi poss\u00edvel descarregar o ficheiro.",
  "assistant.file.entrance": "Relat\u00f3rio de entradas",
  "assistant.file.visitors": "Lista de visitantes com c\u00f3digos QR",
  "assistant.file.allVisitors": "Todos os visitantes inscritos",
  "assistant.file.oneDay": "{day}",
  "assistant.file.range": "{from} a {to}",
};
