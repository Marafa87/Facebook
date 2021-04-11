CREATE (adoubiacho:Person {id:'dc08c867-c436-436f-a9a1-71929d955e7c',surname:'Acho',firstname:'Adoubi',email:'adoubi.acho@gmail.com',phone_number:'06 77 77 88 88',date_of_birth:'01/01/1850',password:'password',created_at:'03/04/2021'})
CREATE (nathfons:Person {id:'f64c47b2-b32d-41a3-9bc6-57f68db7ac0a',surname:'Fons',firstname:'Nathalie',email:'nath.fons@gmail.com',phone_number:'06 88 88 77 77',date_of_birth:'01/01/1980',password:'password',created_at:'03/04/2021'})
CREATE (munirahalafaleq:Person {id:'63f418c7-841a-4ca0-a6bc-558c15eebc2f',surname:'Alafaleq',firstname:'Munirah',email:'muni.alafaleq@gmail.com',phone_number:'06 87 87 57 57',date_of_birth:'01/01/1990',password:'password',created_at:'03/04/2021'})
CREATE (alimarafa:Person {id:'53e87a93-5d40-4229-9721-9da11f098c37',surname:'marafa',firstname:'ali',email:'ali.marafa@gmail.com',phone_number:'07 23 77 88 88',date_of_birth:'02/01/1940',password:'password',created_at:'03/04/2021'})
CREATE (joeldupont:Person {id:'dfeefcdf-aec7-403a-9471-eb802048efd2',surname:'Dupont',firstname:'Joel',email:'joel.dupontq@gmail.com',phone_number:'06 87 87 57 57',date_of_birth:'01/01/1992',password:'password',created_at:'03/04/2021'})


CREATE (profileadoubi:Media{id:'1801abc1-89c8-41f3-bc01-92392f682f1f',local_path:'./img/profile_1801abc1-89c8-41f3-bc01-92392f682f1f.jpg',category:'PHOTO',created_at:'02/04/2021'})
CREATE (backgroundadoubi:Media{id:'97b8aae3-a073-46b0-90ee-3dfc90e149ca',local_path:'./img/background_97b8aae3-a073-46b0-90ee-3dfc90e149ca.jpg',category:'PHOTO',created_at:'02/04/2021'})
CREATE (photo1adoubi:Media{id:'aa33a24b-6543-49c9-9a9d-1593bb14dd7a',local_path:'./img/pic_aa33a24b-6543-49c9-9a9d-1593bb14dd7a.jpg',category:'PHOTO',created_at:'02/04/2021'})

CREATE (profilemapageculturelle:Media{id:'3acf7e74-f2da-4079-88a8-1ad551d94e37',local_path:'./img/profile_3acf7e74-f2da-4079-88a8-1ad551d94e37.jpg',category:'PHOTO',created_at:'02/04/2021'})
CREATE (backgroundmapageculturelle:Media{id:'4317e459-3a6b-4425-8320-f3eaf617dca4',local_path:'./img/background_4317e459-3a6b-4425-8320-f3eaf617dca4.jpg',category:'PHOTO',created_at:'02/04/2021'})
CREATE (photo1mapageculturelle:Media{id:'7c3c9f43-8e84-44a1-a833-73c9ae4dc93a',local_path:'./img/pic_7c3c9f43-8e84-44a1-a833-73c9ae4dc93a.jpg',category:'PHOTO',created_at:'02/04/2021'})


CREATE (adoubiacho)-[:HAS_PROFILE_PICTURE]->(profileadoubi)
CREATE (adoubiacho)-[:HAS_BACKGROUND_PICTURE]->(backgroundadoubi)
CREATE (adoubiacho)-[:OWNS]->(photo1adoubi)

CREATE (adoubiacho)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'ACCEPTED'}]->(nathfons)
CREATE (adoubiacho)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'ACCEPTED'}]->(munirahalafaleq)
CREATE (adoubiacho)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'ACCEPTED'}]->(alimarafa)
CREATE (nathfons)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'ACCEPTED'}]->(munirahalafaleq)
CREATE (nathfons)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'ACCEPTED'}]->(alimarafa)
CREATE (alimarafa)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'ACCEPTED'}]->(munirahalafaleq)
CREATE (joeldupont)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'PENDING'}]->(munirahalafaleq)
CREATE (alimarafa)-[:FRIEND_REQUEST {created_at:'01/04/2021',status:'PENDING'}]->(joeldupont)


CREATE(maPageCulturelle:Page {id:'bdd271e1-8920-4e12-928a-fdc11f6d9813',name_page:' RDVs Culturels',about:'blablablablablablablablablablabla',url_website:'https://mysuperpage.com',type:'READING_PUBLIC',created_at:'03/04/2021'})
CREATE (munirahalafaleq)-[:OWNS_PAGE]->(maPageCulturelle)
CREATE (nathfons)-[:FOLLOWS_PAGE]->(maPageCulturelle)

CREATE (maPageCulturelle)-[:HAS_PROFILE_PICTURE]->(profilemapageculturelle)
CREATE (maPageCulturelle)-[:HAS_BACKGROUND_PICTURE]->(backgroundmapageculturellei)
CREATE (maPageCulturelle)-[:OWNS]->(photo1mapageculturelle)

CREATE(mynews:Post {id:'bdd271e1-8920-4e12-928a-fdc11f6d9813',type:'POST_ON_PAGE_WALL',html_content:'<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'03/04/2021'})

CREATE(mynews2:Post {id:'6b501cb9-785f-474e-bc32-7d0ed7b345b1',type:'POST_ON_PERSON_WALL',html_content:'<!DOCTYPE html><html><body><h1>My Second Heading</h1><p>My second paragraph.</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'04/04/2021'})

CREATE(mynews3:Post {id:'55461adc-7670-4361-b8fb-913e628ca6e2',type:'POST_ON_PERSON_WALL',html_content:'<!DOCTYPE html><html><body><h1>My Third Heading</h1><p>My third paragraph.</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'
})

CREATE(mynews4:Post {id:'007b2437-b05d-4ad8-b9f1-ec4a074aee9f',type:'POST_ON_PERSON_WALL',html_content:'<!DOCTYPE html><html><body><h1>My Fourth Heading</h1><p>My third paragraph.</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'
})

CREATE (adoubiacho)-[:POSTED]->(mynews)
CREATE (adoubiacho)-[:POSTED]->(mynews2)
CREATE (nathfons)-[:POSTED]->(mynews3)
CREATE (nathfons)-[:POSTED]->(mynews4)

CREATE (mynews)-[:DISPLAYED_ON_WALL_OF]->(maPageCulturelle)
CREATE (mynews2)-[:DISPLAYED_ON_WALL_OF]->(maPageCulturelle)
CREATE (mynews3)-[:DISPLAYED_ON_WALL_OF]->(nathfons)
CREATE (mynews4)-[:DISPLAYED_ON_WALL_OF]->(adoubiacho)

CREATE(potes:Group {id:'a7f622d3-bd7b-4bad-9b40-43f2d3156967',group_name:'potes',visibility:'PRIVATE',created_at:'03/04/2021'})
CREATE(boulot:Group {id:'c83a171b-efa7-4f45-b701-5174da104925',group_name:'boulot',visibility:'PRIVATE',created_at:'03/04/2021'})

CREATE (nathfons)-[:OWNS]->(potes)
CREATE (nathfons)-[:OWNS]->(boulot)
CREATE (adoubiacho)-[:IS_MEMBER]->(potes)
CREATE (munirahalafaleq)-[:IS_MEMBER]->(potes)
CREATE (alimarafa)-[:IS_MEMBER]->(potes)
CREATE (adoubiacho)-[:IS_MEMBER]->(boulot)

CREATE (mynews4)-[:SHARED_WITH]->(potes)

CREATE(whoua:Comment {id:'1ae38f34-1e1a-4054-9764-0a59bbcb3465',html_content:'<!DOCTYPE html><html><body><h1>C\'est super!</h1><p>Bravo!</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})

CREATE(smiley:Comment {id:'afa9da29-77ff-4612-a603-a538e37d89ec',icon_emoji_path:'https://www.bing.com/images/search?view=detailV2&ccid=+oBj+2oh&id=AC71D36B15928E65D234E112BFBEBE8D791DA751&thid=OIP.-oBj-2ohpEDlIatP_7_vdgHaHO&mediaurl=https%3A%2F%2Fih1.redbubble.net%2Fimage.415929123.6986%2Fflat%2C800x800%2C075%2Cf.u1.jpg&exph=586&expw=600&q=Laughing+Emoji&simid=608042364165756798&ck=F93493F115F8F9CA1BDF641BD46165F4&selectedindex=26&form=EX0023&adlt=demote&shtp=GetUrl&shid=0d45d515-c29f-4d61-ba12-278783a4c890&shtk=IkNyeWluZyBMYXVnaGluZyBFbW9qaSBTdGlja2VycyEiIFN0aWNrZXJzIGJ5IEhhcnJ5IEZlYXJucyAuLi4%3D&shdk=VHJvdXbDqWUgc3VyIEJpbmcgc3VyIHd3dy5yZWRidWJibGUuY29t&shhk=e3KfF8c3MdZwpSS0gbofpjM3PTWvnL21PilWEM4DUkw%3D&shth=OSH.zneKekg4Zh42ExTP0Z6x2Q',created_at:'05/04/2021'})

CREATE(smiley2:Comment {id:'65668fee-b863-4e2d-b0da-e27f7a73963e',icon_emoji_path:'https://www.bing.com/images/search?view=detailV2&ccid=+oBj+2oh&id=AC71D36B15928E65D234E112BFBEBE8D791DA751&thid=OIP.-oBj-2ohpEDlIatP_7_vdgHaHO&mediaurl=https%3A%2F%2Fih1.redbubble.net%2Fimage.415929123.6986%2Fflat%2C800x800%2C075%2Cf.u1.jpg&exph=586&expw=600&q=Laughing+Emoji&simid=608042364165756798&ck=F93493F115F8F9CA1BDF641BD46165F4&selectedindex=26&form=EX0023&adlt=demote&shtp=GetUrl&shid=0d45d515-c29f-4d61-ba12-278783a4c890&shtk=IkNyeWluZyBMYXVnaGluZyBFbW9qaSBTdGlja2VycyEiIFN0aWNrZXJzIGJ5IEhhcnJ5IEZlYXJucyAuLi4%3D&shdk=VHJvdXbDqWUgc3VyIEJpbmcgc3VyIHd3dy5yZWRidWJibGUuY29t&shhk=e3KfF8c3MdZwpSS0gbofpjM3PTWvnL21PilWEM4DUkw%3D&shth=OSH.zneKekg4Zh42ExTP0Z6x2Q',created_at:'05/04/2021'})
CREATE(whoua2:Comment {id:'06f98cf8-0053-41bc-b2ec-912721c381b6',html_content:'<!DOCTYPE html><html><body><h1>C\'est super!</h1><p>Génial!</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'06/04/2021'})
CREATE(dac:Comment {id:'4006fbf3-803a-4cd9-a5a9-889e9d4165f5',html_content:'<!DOCTYPE html><html><body><h1>C\'est super!</h1><p>Je valide!</p></body></html>',created_at:'06/04/2021'})


CREATE (whoua)-[:COMMENTED]->(mynews)
CREATE (smiley)-[:COMMENTED]->(mynews2)
CREATE (smiley2)-[:COMMENTED]->(mynews3)
CREATE (whoua2)-[:COMMENTED]->(backgroundmapageculturelle)
CREATE (dac)-[:COMMENTED]->(whoua2)


CREATE (smiley)-[:BELONGSTO]->(munirahalafaleq)
CREATE (smiley2)-[:BELONGSTO]->(alimarafa)
CREATE (whoua)-[:BELONGSTO]->(nathfons)
CREATE (whoua2)-[:BELONGSTO]->(adoubiacho)
CREATE (dac)-[:BELONGSTO]->(munirahalafaleq)


CREATE(photo:Media {id:'70f1457c-8a64-4b76-aa27-61e264b0beae',local_path:'./img/earth_70f1457c-8a64-4b76-aa27-61e264b0beae.jpg',created_at:'05/04/2021',category:'PHOTO'})

CREATE(video:Media {id:'d82f12e3-a976-4bc9-9c14-90ec6e664f9c',local_path:'./img/earth_70f1457c-8a64-4b76-aa27-61e264b0beae.mp4',created_at:'05/04/2021',category:'VIDEO'})


CREATE(message:Message {id:'9b7a8061-ee8f-4d0f-a9b6-6803eacc8a26',html_content:'<!DOCTYPE html><html><body><h1>C\'est super!</h1><p>Bravo!</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})


CREATE(bravo:Message {id:'bf0c0243-1ae4-4fa9-a6e1-2298f19fb629',html_content:'<!DOCTYPE html><html><body><h1>C\'est super!</h1><p>Bravo2!!!!!!!</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})



CREATE(rdv:Message {id:'cce13ed6-2e78-4311-a375-d01eb9f325db',html_content:'<!DOCTYPE html><html><body><h1>Hello!</h1><p>On se prend un caf\' demain?</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})

CREATE(rdv2:Message {id:'41ad353a-5323-4850-952b-57f11507f4d8',html_content:'<!DOCTYPE html><html><body><h1>Hello!</h1><p>Ok pr un caf\' !</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})
CREATE(rdv3:Message {id:'057b1411-842c-4816-ba2b-8831f931cbdf',html_content:'<!DOCTYPE html><html><body><h1>Hello!</h1><p>Ok pr un caf\' !</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})
CREATE(rdv4:Message {id:'de262385-1a40-4d3a-9003-17563e69a6b8',html_content:'<!DOCTYPE html><html><body><h1>Hello!</h1><p>Ok pr un caf\' !</p><img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32"></body></html>',created_at:'05/04/2021'})


CREATE (adoubiacho)-[:SENT_MESSAGE]->(message)
CREATE (message)-[:RECIPIENT]->(nathfons)
CREATE (message)-[:RECIPIENT]->(munirahalafaleq)
CREATE (bravo)-[:REPLIED{sender:'munirahalafaleq'}]->(message)

CREATE (alimarafa)-[:SENT_MESSAGE]->(rdv)
CREATE (rdv)-[:RECIPIENT]->(nathfons)
CREATE (rdv)-[:RECIPIENT]->(adoubiacho)
CREATE (rdv)-[:RECIPIENT]->(munirahalafaleq)
CREATE (rdv2)-[:REPLIED{sender:'adoubiacho'}]->(rdv)
CREATE (rdv3)-[:REPLIED{sender:'munirahalafaleq'}]->(rdv2)
CREATE (rdv4)-[:REPLIED{sender:'munirahalafaleq'}]->(rdv3)

CREATE (munirahalafaleq)-[:OWNS]->(photo)
CREATE (alimarafa)-[:OWNS]->(video)
