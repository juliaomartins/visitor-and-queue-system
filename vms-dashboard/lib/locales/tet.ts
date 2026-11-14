import type { Messages } from "./en";

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
export const tet: Messages = {

  // --------------------------------------------------------------- shell --
  "nav.sections": "Seksaun sira",
  "nav.group.overview": "Vizaun jer\u00e1l",
  "nav.group.accreditation": "Akreditasaun",
  "nav.group.operations": "Operasaun",
  "nav.dashboard": "Pain\u00e9l",
  "nav.dashboard.hint": "Xegada no estadu odamatan",
  "nav.visitors": "Vizitante sira",
  "nav.visitors.hint": "Rejistu no f\u00f3 sai kartaun",
  "nav.badges": "Kartaun",
  "nav.badges.hint": "Fila ba impresaun",
  "nav.devices": "Aparellu sira",
  "nav.devices.hint": "Odamatan no ekr\u00e1n",
  "nav.reports": "Relat\u00f3riu",
  "nav.reports.hint": "Rejistu tama",
  "nav.expand": "Loke menu",
  "nav.collapse": "Taka menu",
  "nav.signOut": "Sai",
  "nav.signingOut": "Sai hela\u2026",
  "nav.settings": "Konfigurasaun",
  "nav.settings.hint": "Servidor no hahalok",
  "nav.silentDevices": "Aparellu {count} seidauk komunika",
  "shell.restoringSession": "Restaura sesaun hela",
  "topbar.localTime": "Oras lok\u00e1l",

  // --------------------------------------------------------- preferences --
  "theme.toDark": "Troka ba modu nakukun",
  "theme.toLight": "Troka ba modu naroman",
  "theme.dark": "Nakukun",
  "theme.light": "Naroman",
  "language.label": "Lian",
  "language.choose": "Hili lian",

  // --------------------------------------------------------------- login --
  "login.title": "Tama",
  "login.intro":
    "Konta administrad\u00f3r deit. Seguransa sira uza telem\u00f3vel ne\u2019eb\u00e9 pareia ona, no ekr\u00e1n resepsaun pareia an rasik.",
  "login.username": "Naran uzu\u00e1riu",
  "login.password": "Liafuan-xave",
  "login.submit": "Tama",
  "login.submitting": "Tama hela\u2026",
  "login.badCredentials": "Naran uzu\u00e1riu ho liafuan-xave la hanesan.",
  "login.failedStatus": "La konsege tama (HTTP {status}).",
  "login.unreachable":
    "La bele kontaktu servid\u00f3r. Verifika se backend la\u2019o hela.",
  "login.servingFrom": "Husi",
  "login.pitch":
    "Rejista vizitante, imprime nia kartaun, no haree xegada hotu iha fatin ida \u2014 iha ita-nia rede rasik, laiha buat ida sai husi edif\u00edsiu.",

  // -------------------------------------------------------------- errors --
  "error.unexpected": "Iha erru ida.",
  "error.fields": "Iha kampu balu presiza hadia.",
  "error.visitorLoad": "La bele karga vizitante ne\u2019e.",
  "error.visitorRegister": "La bele rejista vizitante ne\u2019e.",
  "error.visitorSave": "La bele rai mudansa sira.",
  "error.visitorActivate": "La bele ativa vizitante ne\u2019e.",
  "error.visitorDeactivate": "La bele dezativa vizitante ne\u2019e.",
  "error.visitorDelete": "La bele hasai vizitante ne\u2019e.",

  // -------------------------------------------------------- visitor list --
  "visitors.title": "Vizitante sira",
  "visitors.subtitle": "Ema hotu ne\u2019eb\u00e9 rejista ba eventu",
  "visitors.search": "Buka vizitante",
  "visitors.searchPlaceholder":
    "Naran, organizasaun, nasaun ka n\u00fameru kartaun",
  "visitors.filterCategory": "Filtra tuir kategoria",
  "visitors.tab.all": "Hotu",
  "visitors.tab.normal": "Norm\u00e1l",
  "visitors.tab.vip": "VIP",
  "visitors.exportTitle":
    "Ema hotu ne\u2019eb\u00e9 rejista, ho foto no QR kartaun. La f\u00f3 sai kartaun foun.",
  "visitors.exporting": "Esporta hela\u2026",
  "visitors.export": "Esporta Excel",
  "visitors.exportFailed": "La bele esporta lista.",
  "visitors.register": "Rejista vizitante",
  "visitors.refreshing": "Atualiza hela\u2026",
  "visitors.loadFailed": "La bele karga vizitante sira",
  "visitors.requestFailed": "Pedidu falla molok to\u2019o servid\u00f3r.",
  "visitors.serverRejected": "Servid\u00f3r rejeita pedidu ne\u2019e.",
  "visitors.noneMatch": "Laiha ema ida tuir filtru sira ne\u2019e",
  "visitors.noneMatchBody":
    "Koko buka ho liafuan badak liu, ka loke kategoria.",
  "visitors.empty": "Seidauk iha vizitante",
  "visitors.emptyBody": "Rejista vizitante primeiru atu f\u00f3 sai kartaun.",
  "visitors.menu.edit": "Edita dadus",
  "visitors.menu.deactivate": "Dezativa vizitante",
  "visitors.menu.activate": "Ativa vizitante",
  "visitors.menu.delete": "Hasai permanente",
  "visitors.status.deactivated": "Dezativadu",

  // --------------------------------------------------- deactivate dialog --
  "deactivate.title": "Dezativa {name}?",
  "deactivate.body":
    "Kartaun {serial} para funsiona kedas. Leitura tuirmai sei mosu mean iha odamatan.",
  "deactivate.point1":
    "Sira sei hela iha lista vizitante, ho marka dezativadu.",
  "deactivate.point2": "Ist\u00f3ria leitura sei rai nafatin.",
  "deactivate.point3":
    "Bele fila fali. Ativa f\u00f3 fila kartaun ne\u2019eb\u00e9 imprime ona ba servisu \u2014 laiha buat atu imprime fali.",
  "deactivate.cancel": "Rai ativu nafatin",
  "deactivate.confirm": "Dezativa",
  "deactivate.pending": "Dezativa hela\u2026",

  // -------------------------------------------------------- purge dialog --
  "purge.warning": "La bele fila fali",
  "purge.title": "Hasai {name} permanente?",
  "purge.body":
    "Ne\u2019e hasai rejistu no vizitante nia foto husi servid\u00f3r. Dezativa mak opsaun ne\u2019eb\u00e9 bele fila fali; ida ne\u2019e lae.",
  "purge.scansUnknown":
    "Leitura kartaun ne\u2019e nian sei hela iha rejistu tama, maib\u00e9 la naran ema ida ona.",
  "purge.scansNone":
    "Laiha leitura ida afetadu \u2014 kartaun ne\u2019e seidauk aprezenta.",
  "purge.scansOne":
    "Leitura {count} sei hela iha rejistu tama, maib\u00e9 la naran ema ida ona.",
  "purge.scansMany":
    "Leitura {count} sei hela iha rejistu tama, maib\u00e9 la naran ema ida ona.",
  "purge.serialRetired":
    "Kartaun {serial} hasai ona. N\u00fameru ne\u2019e la uza fali.",
  "purge.reRegister":
    "Rejista fila sira sei kria vizitante foun, n\u00fameru foun no QR foun.",
  "purge.typeToConfirm": "Hakerek {serial} atu konfirma",
  "purge.cancel": "Kansela",
  "purge.confirm": "Hasai permanente",
  "purge.pending": "Hasai hela\u2026",

  // ------------------------------------------------------ visitor detail --
  "common.loading": "Karga hela\u2026",
  "visitor.fallbackTitle": "Vizitante",
  "visitor.notFound": "La bele karga vizitante ne\u2019e",
  "visitor.notFoundBody": "Karik hasai tiha ona. Haree lista vizitante.",
  "visitor.backToAll": "Fila ba vizitante hotu",
  "visitor.allVisitors": "Vizitante hotu",
  "visitor.status.active": "Ativu",
  "visitor.headingActive": "Kartaun ne\u2019e loke odamatan",
  "visitor.headingOff": "Kartaun ne\u2019e desliga ona",
  "visitor.subActive":
    "Leit\u00f3r ne\u2019eb\u00e9 pareia ona sei simu, no ekr\u00e1n resepsaun sei f\u00f3 benvindu.",
  "visitor.subOff":
    "Leitura tuirmai sei mosu mean. Ativa f\u00f3 fila kartaun hanesan ba servisu \u2014 la presiza imprime fali.",
  "visitor.registered": "Rejista",
  "visitor.arrivals": "Xegada",
  "visitor.lastArrival": "Xegada ikus",
  "visitor.notYet": "Seidauk",
  "visitor.scansLogged": "Leitura rejistadu",
  "visitor.activating": "Ativa hela\u2026",
  "visitor.qrNote":
    "QR ne\u2019e kria bainhira rejista vizitante no nunka muda. Imprime fali kartaun dala hira mak presiza \u2014 nia lee hanesan beibeik. Dezativa para nia, no ativa hah\u00fa fali, rua ne\u2019e la book k\u00f3digu iha kartaun. Hasai permanente mak buat ida deit iha ne\u2019e ne\u2019eb\u00e9 la bele fila fali.",
  "visitor.scanHistory": "Ist\u00f3ria leitura",
  "visitor.scanHistoryBody":
    "Dala hotu kartaun ne\u2019e aprezenta, inklui dala ne\u2019eb\u00e9 rejeita.",
  "visitor.noScans": "Kartaun ne\u2019e seidauk lee.",
  "visitor.col.event": "Eventu",
  "visitor.col.scannedAt": "Lee iha",
  "visitor.col.result": "Rezultadu",
  "visitor.col.device": "Aparellu",
  "scan.valid": "V\u00e1lidu",
  "scan.duplicate": "Duplikadu",
  "scan.revoked": "Revogadu",
  "scan.invalid": "Inv\u00e1lidu",

  // --------------------------------------------------- registration form --
  "register.title": "Rejista vizitante ida",
  "register.subtitle": "Kartaun ida, imprime uluk, v\u00e1lidu ba eventu tomak",
  "register.issuedTitle": "Kartaun f\u00f3 sai ona",
  "register.issuedSubtitle":
    "Imprime kartaun agora, ka depois husi vizitante nia p\u00e1jina",
  "form.photoRequired": "Kartaun presiza foto. Tau ida molok rejista.",
  "form.fullName": "Naran kompletu",
  "form.fullNameHint": "Hanesan ne\u2019eb\u00e9 tenke mosu iha kartaun.",
  "form.country": "Nasaun",
  "form.organisation": "Organizasaun",
  "form.optional": "Opsion\u00e1l.",
  "form.category": "Kategoria",
  "form.cat.normal": "Norm\u00e1l",
  "form.cat.normalNote": "Kartaun norm\u00e1l",
  "form.cat.vip": "VIP",
  "form.cat.vipNote": "Kartaun espesi\u00e1l no benvindu iha resepsaun",
  "form.registering": "Rejista hela\u2026",
  "form.saving": "Rai hela\u2026",
  "form.register": "Rejista no f\u00f3 sai kartaun",
  "form.save": "Rai mudansa",
  "form.noteCreate":
    "N\u00fameru f\u00f3 bainhira rejista. QR kria iha momentu hanesan no nunka muda depois.",
  "form.noteEdit":
    "Edita dadus la f\u00f3 sai kartaun foun. N\u00fameru no k\u00f3digu QR sei hanesan ho ne\u2019eb\u00e9 imprime ona.",

  // ------------------------------------------------------- badge receipt --
  "receipt.badgeIssued": "Kartaun f\u00f3 sai ona",
  "receipt.registered": "{name} rejista ona",
  "receipt.permanent":
    "QR ne\u2019e permanente. Nia kria bainhira rejista {name} no sei la muda \u2014 imprime agora, ka depois husi nia p\u00e1jina, dala hira mak presiza. Nia para funsiona deit se dezativa ka hasai vizitante.",
  "receipt.qrAlt": "K\u00f3digu QR ba kartaun {serial}",
  "receipt.badgeToken": "Token kartaun",
  "receipt.rendering": "Kria hela\u2026",
  "receipt.downloadPdf": "Deskarrega PDF kartaun",
  "receipt.print": "Imprime kartaun",
  "receipt.printFellBack":
    "Pop-up bloke hela ba site ne\u2019e, tan ne\u2019e kartaun deskarrega ona. Loke fixeiru no imprime husi ne\u2019eb\u00e1.",
  "receipt.copied": "Kopia ona",
  "receipt.copyToken": "Kopia token",
  "receipt.qrFailed":
    "La bele dezenha k\u00f3digu QR. Kopia token no imprime kartaun iha makina seluk, duke f\u00f3 sai kartaun laiha k\u00f3digu.",
  "receipt.copiedAnnounce":
    "Token kartaun kopia ba \u00e1rea transfer\u00e9nsia.",
  "receipt.badgeSerial": "N\u00fameru kartaun",
  "receipt.registerAnother": "Rejista vizitante seluk",
  "receipt.open": "Loke {name}",
  "receipt.renderFailed": "La bele kria kartaun.",

  // ---------------------------------------------------------------- edit --
  "edit.title": "Edita {name}",
  "edit.fallbackTitle": "Edita vizitante",

  // ----------------------------------------------- photo upload and crop --
  "photo.label": "Foto",
  "photo.spec": "3:4 VERTIK\u00c1L \u00b7 600 \u00d7 800",
  "photo.notImage": "Ne\u2019e la\u2019\u00f3s imajen. Hili JPEG ka PNG.",
  "photo.tooLarge": "Imajen ne\u2019e liu 20 MB. Hili ida ki\u2019ik liu.",
  "photo.alt": "Vizitante nia foto kartaun",
  "photo.ready": "Korta ona no prontu.",
  "photo.onFile":
    "Foto ne\u2019eb\u00e9 rai ona. Nia sei hela to\u2019o ita troka.",
  "photo.adjustCrop": "Ajusta korta",
  "photo.chooseDifferent": "Hili foto seluk",
  "photo.add": "Tau foto",
  "photo.dropHint":
    "Tau ida iha ne\u2019e, ka klik atu hili. Tuirmai korta nia.",
  "photo.dialogLabel": "Korta vizitante nia foto",
  "photo.frameFace": "Tau oin iha kuadru",
  "photo.closeWithoutSaving": "Taka la rai",
  "crop.alt": "Foto ne\u2019eb\u00e9 korta hela",
  "crop.preview": "Imajen korta",
  "crop.circleHint":
    "S\u00edrkulu deit mak imprime no hatudu iha ekr\u00e1n resepsaun. Tau ulun ho kabaas iha laran.",
  "crop.aspect": "Proporsaun",
  "crop.ratio.badge": "Kartaun (fiksu)",
  "crop.ratio.square": "Kuadradu",
  "crop.ratio.free": "Livre",
  "crop.width": "Luan",
  "crop.height": "Aas",
  "crop.heightLocked": "Aas (fiksu)",
  "crop.tooSmall":
    "Korta ne\u2019e nia luan {width}px. Kartaun imprime foto ho {min}px ba 300dpi, tan ne\u2019e sei mosu la klaru iha kartaun. Korta uitoan deit, ka uza foto boot liu.",
  "crop.quality": "Kualidade imajen",
  "crop.bestCompression": "Kompresaun di\u2019ak liu",
  "crop.bestQuality": "Kualidade di\u2019ak liu",
  "crop.applying": "Aplika hela\u2026",
  "crop.use": "Uza foto ne\u2019e",
  "crop.changeImage": "Troka imajen",

  // -------------------------------------------------------------- badges --
  "badges.title": "Impresaun kartaun",
  "badges.subtitle": "Sia iha folha A4 ida, ho marka korta",
  "badges.loadFailed": "La bele karga lista vizitante.",
  "badges.safeTitle": "Imprime fali seguru",
  "badges.safeBody":
    "Folha ida-idak lori vizitante nia QR ne\u2019eb\u00e9 iha ona, tan ne\u2019e kartaun bele imprime fali dala hira mak presiza no sira ne\u2019eb\u00e9 f\u00f3 ona kontinua funsiona. Atu para kartaun lakon, dezativa vizitante ne\u2019e iha nia p\u00e1jina \u2014 QR nunka muda, tan ne\u2019e ativa fali f\u00f3 fila kartaun hanesan ba servisu.",
  "badges.searchPlaceholder": "Naran, organizasaun, nasaun ka n\u00fameru",
  "badges.clearSelection": "Hamoos hili",
  "badges.selectAll": "Hili hotu ({count})",
  "badges.print": "Imprime",
  "badges.printCount": "Imprime {count}",
  "badges.sheetFailed": "La bele halo folha.",
  "badges.export": "Esporta Excel",
  "badges.fileFailed": "La bele halo fixeiru.",
  "badges.selectedOne": "{count} hili \u00b7 folha A4 {sheets}",
  "badges.selectedMany": "{count} hili \u00b7 folha A4 {sheets}",
  "badges.noMatch": "Laiha vizitante ida tuir buka ne\u2019e.",
  "badges.onSheet": "Iha folha",
  "badges.notPrinting": "La imprime",
  "badges.menu.selection": "Vizitante {count} ne\u2019eb\u00e9 hili",
  "badges.menu.printOne": "Imprime kartaun",
  "badges.menu.printMany": "Imprime kartaun {count}",
  "badges.menu.exportOne": "Esporta ba Excel\u2026",
  "badges.menu.exportMany": "Esporta {count} ba Excel\u2026",

  // ----------------------------------------------- visitors list: source --
  "visitors.filterSource": "Filtra tuir s\u00e9 mak rejistu",
  "visitors.source.all": "Hotu",
  "visitors.source.admin": "Balkaun",
  "visitors.source.self": "Rejistu rasik",
  "visitors.source.desk": "Meza rejistu",
  "visitors.possibleDuplicate": "Bele duplikadu",
  "visitors.possibleDuplicateTitle":
    "Rejistu seluk iha naran no nasaun hanesan.",

  // --------------------------------------- settings: public registration --
  "settings.registration": "Rejistu p\u00fabliku",
  "settings.registrationNote":
    "Permite vizitante sira rejistu an rasik husi sira-nia telem\u00f3vel iha rede eventu nian. Ida-idak rejistu kedas ho kartaun norm\u00e1l.",
  "settings.registrationToggle": "Permite rejistu p\u00fabliku",
  "settings.registrationOpen": "Loke",
  "settings.registrationClosed": "Taka",
  "settings.registrationUrl": "Link rejistu",
  "settings.registrationUrlNote":
    "Telem\u00f3vel tenke iha Wi-Fi eventu nian atu loke.",
  "settings.registrationNoAddress":
    "Seidauk hatene enderesu rede servid\u00f3r nian.",
  "settings.registrationSaveFailed": "La bele muda. Koko fali.",
  "settings.registrationLoadFailed":
    "Servid\u00f3r la hat\u00e1n ba konfigurasaun ida-ne'e. Se foin atualiza, tenke hah\u00fa fali.",
  "settings.registrationSaveQr": "Rai k\u00f3digu QR",
  "settings.registrationUpdated": "Muda ikus iha {time} husi {user}",

  // -------------------------------------------- public registration page --
  "publicRegister.title": "Rejistu ba eventu",
  "publicRegister.intro":
    "Prienxe ita-nia dadus no aumenta foto ida. Ita sei simu k\u00f3digu QR ida atu hatudu iha entrada.",
  "publicRegister.fullName": "Naran kompletu",
  "publicRegister.country": "Nasaun",
  "publicRegister.countryPlaceholder": "Hah\u00fa hakerek ita-nia nasaun",
  "country.listLabel": "Nasaun sira",
  "country.noMatch": "La iha nasaun ne'eb\u00e9 hanesan \u201c{text}\u201d",
  "country.invalid": "Hili ita-nia nasaun husi lista.",
  "publicRegister.organization": "Organizasaun (opsion\u00e1l)",
  "publicRegister.photo": "Ita-nia foto",
  "publicRegister.photoHint":
    "Hateke ba k\u00e1mara iha naroman di\u2019ak, la iha ema seluk iha imajen.",
  "publicRegister.choosePhoto": "Foti ka hili foto",
  "publicRegister.useCamera": "Uza k\u00e1mara",
  "publicRegister.capture": "Foti foto",
  "publicRegister.cancel": "Kansela",
  "publicRegister.cameraFailed": "La bele loke k\u00e1mara.",
  "publicRegister.changePhoto": "Muda foto",
  "publicRegister.reviewPhoto": "Tesi ita-nia foto",
  "publicRegister.usePhoto": "Uza foto ida-ne\u2019e",
  "publicRegister.retakePhoto": "Foti foto fali",
  "publicRegister.cropTooSmall":
    "Ki\u2019ik liu atu imprime. Dada kantu sira ba li\u2019ur.",
  "publicRegister.checkingFace": "Verifika hela foto\u2026",
  "publicRegister.faceNone":
    "La hetan oin. Hateke ba k\u00e1mara iha naroman di\u2019ak no koko fali.",
  "publicRegister.faceMany":
    "Hetan oin liu ida. Tenke ita mesak de\u2019it iha foto.",
  "publicRegister.faceOk": "Foto di\u2019ak.",
  "publicRegister.consent":
    "Ita-nia foto no dadus uza ba asesu eventu nian no sei hamoos depois eventu.",
  "publicRegister.submit": "Rejistu",
  "publicRegister.submitting": "Rejistu hela\u2026",
  "publicRegister.loading": "Karrega hela\u2026",
  "publicRegister.closedTitle": "Rejistu taka ona",
  "publicRegister.closedBody": "Fav\u00f3r ba balkaun rejistu.",
  "publicRegister.unreachable":
    "La bele liga ba servid\u00f3r eventu nian. Haree katak ita iha Wi-Fi eventu nian.",
  "publicRegister.unavailableTitle": "Rejistu la dispon\u00edvel agora",
  "publicRegister.failed":
    "Rejistu la susesu. Koko fali, ka ba balkaun rejistu.",
  "publicRegister.tooMany":
    "Rejistu barak liu husi koneksaun ne\u2019e. Fav\u00f3r ba balkaun rejistu.",
  "publicRegister.tooLarge": "Foto boot liu. Hili seluk.",
  "publicRegister.successTitle": "Ita rejistu ona",
  "publicRegister.successShow": "Hatudu k\u00f3digu QR ne\u2019e iha entrada.",
  "publicRegister.brightness":
    "Hasa\u2019e naroman ekr\u00e1n nian molok eskaneia.",
  "publicRegister.deskHelp":
    "Se eskaneia la la\u2019o, ba balkaun no temi {serial}.",
  "publicRegister.keepPage":
    "Husik p\u00e1jina ne\u2019e loke to\u2019o ita tama.",
  "publicRegister.qrAlt": "K\u00f3digu QR ba kartaun {serial}",
  "publicRegister.saveTitle": "Rai iha ita-nia telem\u00f3vel",
  "publicRegister.saveBody":
    "Rai k\u00f3digu atu ita sei iha, maski p\u00e1jina ne\u2019e taka.",
  "publicRegister.saveQr": "Rai k\u00f3digu QR",
  "publicRegister.savingQr": "Prepara hela\u2026",
  "publicRegister.saveDone": "Rai ona iha ita-nia telem\u00f3vel.",
  "publicRegister.saveOpened": "Kaer kleur imajen, depois hili Rai imajen.",
  "publicRegister.saveFailed":
    "La bele rai. Foti kaptura ekr\u00e1n husi p\u00e1jina ne\u2019e.",
  "publicRegister.closedNow":
    "Rejistu foin taka. B\u00e1 meza rejistu atu remata.",
  "publicRegister.takePhoto": "Foti foto",
  "publicRegister.chooseFromGallery": "Hili husi galeria",

  // ------------------------------------------------------- export dialog --
  "export.titleOne": "Esporta k\u00f3digu kartaun ba vizitante {count}?",
  "export.titleMany": "Esporta k\u00f3digu kartaun ba vizitante {count}?",
  "export.body":
    "Fixeiru ne\u2019e iha {strong} ba vizitante ida-idak. Esporta la muda buat ida \u2014 k\u00f3digu sira mak ne\u2019eb\u00e9 iha ona sira-nia kartaun \u2014 maib\u00e9 ema ne\u2019eb\u00e9 iha fixeiru bele halo kartaun ne\u2019eb\u00e9 lee.",
  "export.bodyStrong": "k\u00f3digu QR ne\u2019eb\u00e9 funsiona",
  "export.point1":
    "Haruka nia hanesan haruka kartaun imprimidu, la\u2019\u00f3s hanesan haruka lista konvidadu.",
  "export.point2":
    "Esporta fali depois sei halo fixeiru hanesan. Lakon ida ne\u2019e la kustu buat ida, tempu deit atu esporta fali.",
  "export.point3":
    "Atu para kartaun ida, dezativa vizitante ne\u2019e iha nia p\u00e1jina. Hasai fixeiru la para buat ida.",
  "export.building": "Prepara hela\u2026",
  "export.confirm": "Esporta no deskarrega",
  "card.deactivated": "Dezativadu",
  "card.qrOnCard": "iha kartaun imprimidu",
  "card.qrDrawing": "dezenha hela\u2026",
  "card.qrFailed": "la bele dezenha",

  // ------------------------------------------------------------- devices --
  "time.justNow": "foin daudaun",
  "device.kind.scanner": "Leit\u00f3r",
  "device.kind.screen": "Ekr\u00e1n",
  "device.kind.desk": "Meza",
  "device.kindInline.scanner": "leit\u00f3r",
  "device.kindInline.screen": "ekr\u00e1n",
  "device.kindInline.desk": "meza",
  "devices.subtitleQuiet":
    "Seguransa sira-nia telem\u00f3vel no ekr\u00e1n resepsaun",
  "devices.silentOne": "Aparellu {count} seidauk komunika",
  "devices.silentMany": "Aparellu {count} seidauk komunika",
  "devices.alertOne": "Aparellu {count} nonook.",
  "devices.alertMany": "Aparellu {count} nonook.",
  "devices.alertBody":
    "Odamatan ne\u2019eb\u00e9 laiha leitura durante minutu sanulu karik nonook ka offline \u2014 b\u00e1 haree.",
  "devices.paired": "Aparellu ne\u2019eb\u00e9 pareia ona",
  "devices.pairedBody":
    "Atualiza an rasik. \u201cHaree ikus\u201d mak pedidu ikus ne\u2019eb\u00e9 aparellu halo, no ho ne\u2019e mak ita hatene odamatan nonook ka telem\u00f3vel mate.",
  "devices.loadFailed": "La bele karga aparellu",
  "devices.none": "Seidauk iha aparellu pareia",
  "devices.noneBody":
    "Kria k\u00f3digu iha leten, depois tau iha seguransa nia telem\u00f3vel ka ekr\u00e1n resepsaun.",
  "devices.col.device": "Aparellu",
  "devices.col.kind": "Tipu",
  "devices.col.lastSeen": "Haree ikus",
  "devices.col.state": "Estadu",
  "devices.neverCheckedIn": "Nunka komunika",
  "devices.silentCheck": "Nonook \u2014 haree odamatan",
  "devices.notSeenSincePairing": "Laiha sin\u00e1l desde pareia",
  "devices.stateRevoked": "REVOGADU",
  "devices.stateActive": "ATIVU",
  "devices.revoke": "Revoga",

  // ------------------------------------------------------------- pairing --
  "pair.title": "Pareia aparellu ida",
  "pair.body":
    "Loke aplikasaun iha telem\u00f3vel ka ekr\u00e1n, depois lee k\u00f3digu iha okos. K\u00f3digu ida-idak funsiona dala ida deit.",
  "pair.codeButton": "K\u00f3digu {kind}",
  "pair.blurb.scanner": "Seguransa nia telem\u00f3vel, iha odamatan",
  "pair.blurb.screen": "Ekr\u00e1n resepsaun",
  "pair.blurb.desk":
    "Laptop ka tablet ne\u2019eb\u00e9 rejista vizitante iha odamatan",
  "pair.deskLink": "Link meza nian",
  "pair.deskLinkBody":
    "Loke ne\u2019e iha dispozitivu meza nian, depois hakerek k\u00f3digu iha leten. Hatudu de\u2019it dala ida.",
  "pair.deskLinkWarn":
    "Rai link ne\u2019e privadu. Ema ne\u2019eb\u00e9 iha link no k\u00f3digu bele rejista vizitante.",
  "pair.deskLinkNoAddress": "Seidauk hatene enderesu rede servid\u00f3r nian.",
  "pair.copyLink": "Kopia link",
  "pair.copied": "Kopia ona",
  "pair.copyManual": "Hili ona \u2014 hanehan Ctrl+C atu kopia.",
  "pair.codeLabel": "K\u00f3digu pareia {kind}",
  "pair.expired":
    "K\u00f3digu ne\u2019e liu ona tempu. Kria seluk \u2014 laiha buat ida pareia ho nia.",
  "pair.expiresIn": "Liu tempu iha",
  "desk.title": "Meza rejistu",
  "desk.pairTitle": "Pareia meza ne\u2019e",
  "desk.pairBody":
    "Hakerek k\u00f3digu husi painel. Halo ida ne\u2019e dala ida de\u2019it iha dispozitivu ne\u2019e.",
  "desk.codeLabel": "K\u00f3digu pareia",
  "desk.nameLabel": "Naran meza",
  "desk.namePlaceholder": "Entrada prinsip\u00e1l",
  "desk.nameHint":
    "Fatin meza ne\u2019e. Administrad\u00f3r haree iha lista dispozitivu.",
  "desk.pair": "Pareia",
  "desk.pairing": "Pareia hela\u2026",
  "desk.pairFailed": "K\u00f3digu ne\u2019e la simu.",
  "desk.formTitle": "Rejista vizitante ida",
  "desk.fullName": "Naran kompletu",
  "desk.country": "Nasaun",
  "desk.organization": "Organizasaun (opsion\u00e1l)",
  "desk.category": "Tipu kartaun",
  "desk.normal": "Norm\u00e1l",
  "desk.vip": "VIP",
  "desk.photo": "Foto vizitante nian",
  "desk.photoHint": "Foti foto, ka hili ida husi dispozitivu ne\u2019e.",
  "desk.register": "Rejista vizitante",
  "desk.registering": "Rejista hela\u2026",
  "desk.doneTitle": "Rejista ona",
  "desk.showQr": "Husu vizitante atu foti foto k\u00f3digu ne\u2019e.",
  "desk.keepIt": "Sira hatudu iha entrada, ohin ka aban.",
  "desk.again": "Rejista vizitante seluk",
  "desk.downloadQr": "Deskarega k\u00f3digu QR",
  "desk.downloading": "Prepara hela\u2026",
  "desk.downloadDone": "Rai ona. Fahe ba vizitante.",
  "desk.downloadOpened": "Kaer kleur imajen, depois hili Rai imajen.",
  "desk.downloadFailed":
    "La bele rai. Husu vizitante atu foti foto k\u00f3digu.",
  "desk.qrAlt": "K\u00f3digu QR ba kartaun {serial}",
  "desk.qrFailed":
    "La bele deze\u00f1a k\u00f3digu. Rejista fali vizitante ne\u2019e.",
  "desk.unpaired":
    "Meza ne\u2019e la pareia ona. Husu k\u00f3digu foun ba administrad\u00f3r.",
  "desk.wrongDevice": "K\u00f3digu ne\u2019e ba dispozitivu tipu seluk.",
  "desk.tooMany": "Rejistu barak liu husi meza ne\u2019e. Hein minutu balu.",
  "desk.tooLarge": "Foto boot liu. Hili seluk.",
  "desk.failed": "La bele rejista vizitante. Koko fali.",
  "desk.unreachable": "La bele kontaktu servid\u00f3r eventu nian.",
  "pair.alphabetNote":
    "K\u00f3digu nunka iha 0, O, 1 ka I \u2014 haat ne\u2019e la tau tanba sira mak ema rona sala no hakerek sala. Aparellu mosu iha lista okos bainhira pareia.",

  // ------------------------------------------------ revoke device dialog --
  "revokeDevice.title": "Revoga {name}?",
  "revokeDevice.body":
    "{kind} ne\u2019e para funsiona {strong}. Se nia telem\u00f3vel odamatan nian, odamatan ne\u2019e la bele rejista xegada to\u2019o ema pareia fali.",
  "revokeDevice.bodyStrong": "kedas",
  "revokeDevice.point1":
    "{strong} \u2014 iha segundu balu, la presiza ema b\u00e1. Prepara k\u00f3digu pareia foun se ita hakarak lori nia fila kedas.",
  "revokeDevice.point1Strong": "Nia fila mesak ba ekr\u00e1n pareia",
  "revokeDevice.point2":
    "Nia token mate ona. Laiha dalan atu fila fali \u2014 atu hetan nia fali presiza k\u00f3digu pareia foun.",
  "revokeDevice.point3":
    "Leitura ne\u2019eb\u00e9 nia rejista ona sei rai, no sira ne\u2019eb\u00e9 nia rai offline sei sinkroniza bainhira pareia fali.",
  "revokeDevice.point4":
    "Nia sei hela iha lista ne\u2019e, ho marka revogadu, atu rejistu auditoria nafatin.",
  "revokeDevice.cancel": "Rai ativu nafatin",
  "revokeDevice.pending": "Revoga hela\u2026",
  "revokeDevice.confirm": "Revoga aparellu",
  "error.deviceLoad": "La bele karga lista aparellu.",
  "error.pairingCode": "La bele kria k\u00f3digu pareia.",
  "error.deviceRevoke": "La bele revoga aparellu.",

  // ------------------------------------------------------------- reports --
  "reports.title": "Rejistu tama",
  "reports.subtitleQuiet": "Xegada no rejeisaun",
  "reports.subtitleRefused": "{count} rejeita iha odamatan",
  "reports.subtitleNoRefusals":
    "Laiha kartaun rejeita iha per\u00edodu ne\u2019e",
  "reports.allOutcomes": "Rezultadu hotu",
  "reports.allCategories": "Kategoria hotu",
  "reports.from": "Husi",
  "reports.to": "To\u2019o",
  "reports.outcome": "Rezultadu",
  "reports.any": "Ida-idak",
  "reports.exportNote": "Tuir duni filtru sira iha leten, hanesan hatudu.",
  "reports.preparing": "Prepara hela\u2026",
  "reports.exportFailed": "La bele rai esportasaun.",
  "reports.logFailed": "La bele karga rejistu",
  "reports.everyBadge": "Kartaun hotu ne\u2019eb\u00e9 aprezenta",
  "reports.everyBadgeNote":
    "Li\u00f1a sira iha n\u00fameru leten nia kotuk, inklui rejeisaun",
  "reports.timezone": "Oras hatudu iha {zone}.",
  "reports.format.pdf": "Relat\u00f3riu PDF",
  "reports.format.pdfHint":
    "Relat\u00f3riu hakerek \u2014 deskoberta, gr\u00e1fiku no tabela. Atu haruka ba.",
  "reports.format.xlsx": "Livru Excel",
  "reports.format.xlsxHint":
    "Folha neen, val\u00f3r hanesan n\u00fameru. Ba ema ne\u2019eb\u00e9 hakarak halo an\u00e1lize.",
  "reports.format.csv": "Rejistu CSV",
  "reports.format.csvHint":
    "Rejistu leitura krua, li\u00f1a ida ba kartaun ida-idak. Laiha an\u00e1lize.",
  "reports.export.stale":
    "Esportasaun ne\u2019e seidauk iha servid\u00f3r \u2014 nia la\u2019o versaun tuan liu duke p\u00e1jina ne\u2019e. Hah\u00fa fali backend no koko fali.",
  "reports.export.expired":
    "Ita-nia sesaun liu tempu ona. Karga fali p\u00e1jina no tama fali.",
  "reports.export.serverError":
    "Servid\u00f3r la konsege halo esportasaun ne\u2019e (HTTP {status}).",
  "reports.export.downloadFailed":
    "La bele deskarrega esportasaun ne\u2019e (HTTP {status}).",
  "error.reportLoad": "La bele karga rejistu tama.",

  // --------------------------------------------------------------- recap --
  "recap.unavailable": "An\u00e1lize la disponivel",
  "recap.unavailableBody":
    "Servid\u00f3r hat\u00e1n laiha deskoberta derivadu, katak nia la\u2019o versaun tuan liu duke p\u00e1jina ne\u2019e. Hah\u00fa fali backend no karga fali \u2014 rejistu iha okos la afetadu no loos nafatin.",
  "recap.scans": "Leitura",
  "recap.inRange": "Iha per\u00edodu ne\u2019e",
  "recap.people": "Ema",
  "recap.distinct": "Vizitante la hanesan",
  "recap.duplicates": "Duplikadu",
  "recap.reEntries": "Tama fali, la\u2019\u00f3s rejeisaun",
  "recap.refused": "Rejeita",
  "recap.invalidOrRevoked": "Inv\u00e1lidu ka revogadu",
  "recap.nothingScanned": "Laiha buat lee iha per\u00edodu ne\u2019e",
  "recap.nothingScannedBody":
    "Loke loron barak liu, ka hamoos filtru. Seidauk iha buat atu relata.",
  "recap.attendance": "Prezensa",
  "recap.attendanceNote": "{arrived} husi {registered} rejista",
  "recap.scansLogged": "Leitura rejistadu",
  "recap.repeatNote": "Ema {count} liu dala liu ida",
  "recap.busiestHour": "Oras besik liu",
  "recap.peakNote": "Leitura {total} \u00b7 {share}% husi per\u00edodu",
  "recap.noArrivals": "Laiha xegada rejistadu",
  "recap.refusalNote": "{rate}% husi buat hotu ne\u2019eb\u00e9 aprezenta",
  "recap.noneTurnedAway": "Laiha kartaun rejeita",
  "recap.whatNumbersSay": "N\u00fameru sira hatete saida",
  "recap.whatNumbersSayNote":
    "Kria husi per\u00edodu ne\u2019e \u2014 li\u00f1a ida-idak mak afirmasaun ne\u2019eb\u00e9 dadus sustenta",
  "recap.loadByDoor": "Movimentu tuir odamatan",
  "recap.loadByDoorNote":
    "Odamatan ida ne\u2019eb\u00e9 rejeita kartaun mak odamatan ho problema",
  "recap.noDoorScan": "Laiha odamatan rejista leitura.",
  "recap.refusedHere": "{count} rejeita iha ne\u2019e",
  "recap.notArrived": "Rejista ona, seidauk to\u2019o",
  "recap.notArrivedCount": "{count} husi {registered}",
  "recap.notArrivedNote":
    "Laiha leitura v\u00e1lidu iha per\u00edodu ne\u2019e. Lista kompletu iha PDF no livru Excel.",
  "recap.andMore": "no {count} tan",

  // ----------------------------------------------------------- entry log --
  "entry.emptyBody": "Loke loron barak liu, ka hamoos filtru.",
  "entry.col.time": "Oras",
  "entry.col.name": "Naran",
  "chart.noScans":
    "Laiha leitura iha per\u00edodu ne\u2019e, tan ne\u2019e laiha buat atu hatudu.",
  "chart.refused": "Rejeita",
  "chart.scansByHour": "Leitura tuir oras",

  // ------------------------------------------------------------ overview --
  "overview.subtitleQuiet": "Ohin nia xegada iha odamatan hotu",
  "overview.silentOne":
    "Odamatan {count} nonook ona \u2014 haree Aparellu sira",
  "overview.silentMany":
    "Odamatan {count} nonook ona \u2014 haree Aparellu sira",
  "overview.registered": "Rejista",
  "overview.vipCount": "{count} VIP",
  "overview.arrivedToday": "To\u2019o ohin",
  "overview.arrivedNote": "{percent}% husi sira ne\u2019eb\u00e9 rejista",
  "overview.refusedAtDoor": "Rejeita iha odamatan",
  "overview.duplicateOne": "Leitura duplikadu {count} la konta",
  "overview.duplicateMany": "Leitura duplikadu {count} la konta",
  "overview.doorsReporting": "Odamatan ne\u2019eb\u00e9 komunika",
  "overview.silentCount": "{count} nonook",
  "overview.allCheckedIn": "Hotu komunika foin lalais",
  "overview.arrivalsByHour": "Xegada tuir oras",
  "overview.arrivalsByHourNote":
    "Kartaun hotu ne\u2019eb\u00e9 aprezenta ohin, marka iha oras ne\u2019eb\u00e9 akontese",
  "overview.scanCountOne": "leitura {count}",
  "overview.scanCountMany": "leitura {count}",
  "overview.outcomeSplit": "Divizaun rezultadu",
  "overview.outcomeSplitNote": "Oins\u00e1 ohin nia leitura fahe",
  "overview.recentScans": "Leitura foun sira",
  "overview.recentScansNote": "Foun liu uluk, inklui rejeisaun",
  "overview.nothingToday": "Ohin seidauk lee buat ida.",
  "overview.arrivalsAppear":
    "Xegada mosu iha ne\u2019e bainhira seguransa lee kartaun.",
  "overview.colVisitor": "Vizitante",
  "overview.openLog": "Loke rejistu tama kompletu \u2192",
  "overview.arrivedSummary.oneOne":
    "Ema {people} to\u2019o ho leitura {scans}.",
  "overview.arrivedSummary.oneMany":
    "Ema {people} to\u2019o ho leitura {scans}.",
  "overview.arrivedSummary.manyOne":
    "Ema {people} to\u2019o ho leitura {scans}.",
  "overview.arrivedSummary.manyMany":
    "Ema {people} to\u2019o ho leitura {scans}.",

  // --------------------------------------------------------------- brand --
  "brand.organisedBy": "Organiza husi {first} no {second}.",
  "brand.dates": "D\u00edli, 2\u20133 Outubru 2026",
  "settings.title": "Konfigurasaun",
  "settings.subtitle":
    "Servidor ida ne\u2019e, no oinsa painel ne\u2019e hatudu",
  "settings.server": "Servidor no ligasaun",
  "settings.serverNote":
    "Saida servidor dehan kona-ba nia an. Hatudu telefone no ekr\u00e1n hotu ba enderesu iha kraik.",
  "settings.lanAddress": "Enderesu iha rede",
  "settings.lanAddressNote": "Aparelhu sira liga ba servidor iha ne\u2019e",
  "settings.copy": "Kopia",
  "settings.copied": "Kopia ona",
  "settings.reachable": "Bele hetan",
  "settings.reachableYes": "Responde iha {ms} ms",
  "settings.reachableNo": "La responde",
  "settings.unreachableBody":
    "Painel liga ba nia servidor rasik maibe la liga ba backend. Haree se uvicorn la\u2019o hela.",
  "settings.service": "Servisu",
  "settings.serverClock": "Rel\u00f3jiu servidor",
  "settings.browserClock": "Navegador ne\u2019e",
  "settings.drift": "Diferensa rel\u00f3jiu",
  "settings.driftAhead": "{amount} avansa",
  "settings.driftBehind": "{amount} atrasu",
  "settings.driftLevel": "Hanesan",
  "settings.driftNote":
    "Telefone guarda nian marka nia oras leitura rasik, no relat\u00f3riu grupu sira tuir oras. Rel\u00f3jiu ne\u2019ebe diferensa liu minutu ida bele tau xegada iha oras sala.",
  "settings.checkedAt": "Verifika iha {time}",
  "settings.checkAgain": "Verifika fali",
  "settings.checking": "Verifika hela\u2026",
  "settings.appearance": "Hahalok",
  "settings.appearanceNote":
    "Rai iha navegador ne\u2019e. Meza ida-idak bele hili nian.",
  "settings.themeLabel": "Tema",
  "settings.languageLabel": "Lian",

  // ----------------------------------------------------------- assistant --
  "assistant.launcher": "Husu ba IA",
  "assistant.launcherLabel": "Husu ba IA kona-ba eventu",
  "assistant.title": "Asistente IA",
  "assistant.subtitle": "Resposta mai husi rejistu inskrisaun no tama nian.",
  "assistant.close": "Taka",
  "assistant.newConversation": "Konversa foun",
  "assistant.history": "Ist\u00f3ria",
  "assistant.historyTitle": "Ita-nia konversa sira",
  "assistant.historyEmpty":
    "Seidauk iha konversa rai. Pergunta hotu ne\u2019eb\u00e9 ita husu rai iha ne\u2019e.",
  "assistant.recent": "Konversa foin lalais",
  "assistant.recentHint": "Kontinua husi ne\u2019eb\u00e9 ita para.",
  "assistant.viewAll": "Haree konversa hotu",
  "assistant.untitled": "La iha t\u00edtulu",
  "assistant.backToChat": "Fila ba konversa",
  "assistant.deleteConversation": "Hasai konversa",
  "assistant.rename": "Troka naran",
  "assistant.renameLabel": "Naran konversa",
  "assistant.renameFailed": "La konsege troka naran konversa.",
  "assistant.cancel": "Kansela",
  "assistant.moreActions": "Asaun seluk",
  "assistant.rowHint": "Klik loos atu troka naran ka hasai",
  "assistant.confirmDelete": "Hasai permanente",
  "assistant.loadFailed": "La konsege karrega konversa.",
  "assistant.memoriesTitle": "Hanoin hela",
  "assistant.memoriesHint":
    "Hatete \u201chanoin\u2026\u201d iha pergunta atu aumenta nota ida. Nota la rai dadus vizitante nian.",
  "assistant.memoriesEmpty": "Seidauk hanoin buat ida.",
  "assistant.forget": "Haluha",
  "assistant.remembered": "Hanoin ona: {note}",
  "assistant.emptyLead":
    "Husu ho ita-nia liafuan rasik, ka hah\u00fa ho ida husi ne\u2019e.",
  "assistant.suggest.dayOne":
    "Ema na\u2019in hira mak to\u2019o iha loron 2 Outubru?",
  "assistant.suggest.vipAbsent":
    "Konvidadu VIP sira ne\u2019eb\u00e9 mak la to\u2019o?",
  "assistant.suggest.refused":
    "Se mak hetan rejeisaun iha odamatan, no bainhira?",
  "assistant.suggest.excel":
    "F\u00f3 relat\u00f3riu tama ba loron rua nian iha Excel",
  "assistant.placeholder": "Husu kona-ba xegada, vizitante ka rejeisaun",
  "assistant.send": "Haruka",
  "assistant.inputHint": "Enter atu haruka, Shift+Enter ba li\u00f1a foun",
  "assistant.thinking": "Lee hela rejistu\u2026",
  "assistant.you": "Ita",
  "assistant.bot": "Asistente",
  "assistant.privacy":
    "OpenAI mak hakerek resposta husi rejistu eventu ne\u2019e nian. Foto no k\u00f3digu kartaun nunka haruka.",
  "assistant.disabled":
    "Asistente mate iha servidor ne\u2019e. Aumenta OPENAI_API_KEY ba vms-backend/.env no reinisia backend.",
  "assistant.retry": "Koko fali",
  "assistant.error.throttled":
    "Pergunta barak liu iha minutu ida. Hein uitoan no koko fali.",
  "assistant.error.network":
    "Backend la responde. Haree se nia la\u2019o hela.",
  "assistant.error.stale":
    "Backend seidauk iha asistente. Reinisia nia atu karrega k\u00f3digu foun.",
  "assistant.error.unexpected": "La konsege responde pergunta ne\u2019e.",
  "assistant.download": "Deskarega",
  "assistant.downloading": "Prepara hela\u2026",
  "assistant.downloadFailed": "La konsege deskarega arkivu.",
  "assistant.file.entrance": "Relat\u00f3riu tama",
  "assistant.file.visitors": "Lista vizitante ho k\u00f3digu QR",
  "assistant.file.allVisitors": "Vizitante rejistadu hotu",
  "assistant.file.oneDay": "{day}",
  "assistant.file.range": "{from} to\u2019o {to}",
};
