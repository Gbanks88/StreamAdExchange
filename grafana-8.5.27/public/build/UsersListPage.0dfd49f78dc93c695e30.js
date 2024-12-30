"use strict";(self.webpackChunkgrafana=self.webpackChunkgrafana||[]).push([[8039],{"./public/app/features/users/UsersListPage.tsx":(e,s,t)=>{t.r(s),t.d(s,{UsersListPage:()=>W,default:()=>$});var n=t("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),r=t("./.yarn/__virtual__/react-redux-virtual-7ad20a440e/3/opt/drone/yarncache/react-redux-npm-7.2.6-134f5ed64d-0bf142ce0d.zip/node_modules/react-redux/es/index.js"),a=t("./packages/grafana-data/src/index.ts"),i=t("./packages/grafana-ui/src/index.ts"),c=t("./public/app/core/components/Page/Page.tsx"),l=t("./public/app/core/selectors/navModel.ts"),o=t("./public/app/features/invites/state/actions.ts"),d=t("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/jsx-runtime.js");const h={revokeInvite:o.GY},u=(0,r.connect)(null,h);class p extends n.PureComponent{render(){const{invitee:e,revokeInvite:s}=this.props;return(0,d.jsxs)("tr",{children:[(0,d.jsx)("td",{children:e.email}),(0,d.jsx)("td",{children:e.name}),(0,d.jsxs)("td",{className:"text-right",children:[(0,d.jsx)(i.ClipboardButton,{variant:"secondary",size:"sm",getText:()=>e.url,children:"Copy Invite"})," "]}),(0,d.jsx)("td",{children:(0,d.jsx)(i.Button,{variant:"destructive",size:"sm",icon:"times",onClick:()=>s(e.code)})})]})}}const x=u(p);var m,g,v;class j extends n.PureComponent{render(){const{invitees:e}=this.props;return(0,d.jsxs)("table",{className:"filter-table form-inline",children:[(0,d.jsx)("thead",{children:(0,d.jsxs)("tr",{children:[m||(m=(0,d.jsx)("th",{children:"Email"})),g||(g=(0,d.jsx)("th",{children:"Name"})),v||(v=(0,d.jsx)("th",{})),(0,d.jsx)("th",{style:{width:"34px"}})]})}),(0,d.jsx)("tbody",{children:e.map(((e,s)=>(0,d.jsx)(x,{invitee:e},`${e.id}-${s}`)))})]})}}var b=t("../../opt/drone/yarncache/reselect-npm-4.1.5-bc046e41ae-54c13c1e79.zip/node_modules/reselect/es/index.js"),f=t("./public/app/features/invites/state/reducers.ts");const{selectAll:I,selectById:U,selectTotal:y}=f.wl,w=(0,b.P1)([I,(e,s)=>s],((e,s)=>{const t=new RegExp(s,"i");return e.filter((e=>t.test(e.name)||t.test(e.email)))}));var P=t("./public/app/core/core.ts"),k=t("./public/app/types/index.ts"),C=t("./public/app/features/users/state/reducers.ts");const M=e=>{const s=new RegExp(e.searchQuery,"i");return e.users.filter((e=>s.test(e.login)||s.test(e.email)||s.test(e.name)))},R=e=>e.searchQuery,N=e=>e.searchPage;var S;class L extends n.PureComponent{render(){const{canInvite:e,externalUserMngLinkName:s,externalUserMngLinkUrl:t,searchQuery:n,pendingInvitesCount:r,setUsersSearchQuery:a,onShowInvites:c,showInvites:l}=this.props,o=[{label:"Users",value:"users"},{label:`Pending Invites (${r})`,value:"invites"}],h=P.Vt.hasAccess(k.bW.OrgUsersAdd,e);return(0,d.jsxs)("div",{className:"page-action-bar",children:[(0,d.jsx)("div",{className:"gf-form gf-form--grow",children:(0,d.jsx)(i.FilterInput,{value:n,onChange:a,placeholder:"Search user by login, email or name"})}),r>0&&(0,d.jsx)("div",{style:{marginLeft:"1rem"},children:(0,d.jsx)(i.RadioButtonGroup,{value:l?"invites":"users",options:o,onChange:c})}),h&&(S||(S=(0,d.jsx)(i.LinkButton,{href:"org/users/invite",children:"Invite"}))),t&&(0,d.jsx)(i.LinkButton,{href:t,target:"_blank",rel:"noopener",children:s})]})}}const _={setUsersSearchQuery:C.oX},B=(0,r.connect)((function(e){return{searchQuery:R(e.users),pendingInvitesCount:y(e.invites),externalUserMngLinkName:e.users.externalUserMngLinkName,externalUserMngLinkUrl:e.users.externalUserMngLinkUrl,canInvite:e.users.canInvite}}),_)(L);var A=t("./public/app/features/users/UsersTable.tsx"),z=t("./packages/grafana-runtime/src/index.ts"),O=t("./public/app/core/utils/accessControl.ts");function T(){return async e=>{const s=await(0,z.getBackendSrv)().get("/api/org/users",(0,O.y)());e((0,C.eT)(s))}}function Q(e,s,t){return s in e?Object.defineProperty(e,s,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[s]=t,e}const V={loadUsers:T,fetchInvitees:o.nW,setUsersSearchQuery:C.oX,setUsersSearchPage:C.TQ,updateUser:function(e){return async s=>{await(0,z.getBackendSrv)().patch(`/api/org/users/${e.userId}`,{role:e.role}),s(T())}},removeUser:function(e){return async s=>{await(0,z.getBackendSrv)().delete(`/api/org/users/${e}`),s(T())}}},E=(0,r.connect)((function(e){const s=R(e.users);return{navModel:(0,l.h)(e.navIndex,"users"),users:M(e.users),searchQuery:R(e.users),searchPage:N(e.users),invitees:w(e.invites,s),externalUserMngInfo:e.users.externalUserMngInfo,hasFetched:e.users.hasFetched}}),V);class W extends n.PureComponent{constructor(e){super(e),Q(this,"onRoleChange",((e,s)=>{const t=Object.assign({},s,{role:e});this.props.updateUser(t)})),Q(this,"onShowInvites",(()=>{this.setState((e=>({showInvites:!e.showInvites})))})),Q(this,"getPaginatedUsers",(e=>{const s=30*(this.props.searchPage-1);return e.slice(s,s+30)})),this.props.externalUserMngInfo&&(this.externalUserMngInfoHtml=(0,a.renderMarkdown)(this.props.externalUserMngInfo)),this.state={showInvites:!1}}componentDidMount(){this.fetchUsers(),this.fetchInvitees()}async fetchUsers(){return await this.props.loadUsers()}async fetchInvitees(){return await this.props.fetchInvitees()}renderTable(){const{invitees:e,users:s,setUsersSearchPage:t}=this.props,n=this.getPaginatedUsers(s),r=Math.ceil(s.length/30);return this.state.showInvites?(0,d.jsx)(j,{invitees:e}):(0,d.jsxs)(i.VerticalGroup,{spacing:"md",children:[(0,d.jsx)(A.Z,{users:n,onRoleChange:(e,s)=>this.onRoleChange(e,s),onRemoveUser:e=>this.props.removeUser(e.userId)}),(0,d.jsx)(i.HorizontalGroup,{justify:"flex-end",children:(0,d.jsx)(i.Pagination,{onNavigate:t,currentPage:this.props.searchPage,numberOfPages:r,hideWhenSinglePage:!0})})]})}render(){const{navModel:e,hasFetched:s}=this.props,t=this.externalUserMngInfoHtml;return(0,d.jsx)(c.Z,{navModel:e,children:(0,d.jsx)(c.Z.Contents,{isLoading:!s,children:(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(B,{onShowInvites:this.onShowInvites,showInvites:this.state.showInvites}),t&&(0,d.jsx)("div",{className:"grafana-info-box",dangerouslySetInnerHTML:{__html:t}}),s&&this.renderTable()]})})})}}const $=E(W)},"./public/app/features/users/UsersTable.tsx":(e,s,t)=>{t.d(s,{Z:()=>v});var n,r,a,i,c,l,o=t("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),d=t("./packages/grafana-ui/src/index.ts"),h=t("./public/app/core/components/RolePicker/UserRolePicker.tsx"),u=t("./public/app/core/components/RolePicker/api.ts"),p=t("./public/app/core/core.ts"),x=t("./public/app/types/index.ts"),m=t("./public/app/features/admin/OrgRolePicker.tsx"),g=t("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/jsx-runtime.js");const v=e=>{const{users:s,orgId:t,onRoleChange:v,onRemoveUser:j}=e,[b,f]=(0,o.useState)(null),[I,U]=(0,o.useState)([]),[y,w]=(0,o.useState)({});return(0,o.useEffect)((()=>{p.Vt.licensedAccessControlEnabled()&&async function(){try{if(p.Vt.hasPermission(x.bW.ActionRolesList)){let e=await(0,u.ul)(t);U(e)}if(p.Vt.hasPermission(x.bW.ActionBuiltinRolesList)){const e=await(0,u.fh)(t);w(e)}}catch(e){console.error("Error loading options")}}()}),[t]),(0,g.jsxs)(g.Fragment,{children:[(0,g.jsxs)("table",{className:"filter-table form-inline",children:[(0,g.jsx)("thead",{children:(0,g.jsxs)("tr",{children:[n||(n=(0,g.jsx)("th",{})),r||(r=(0,g.jsx)("th",{children:"Login"})),a||(a=(0,g.jsx)("th",{children:"Email"})),i||(i=(0,g.jsx)("th",{children:"Name"})),c||(c=(0,g.jsx)("th",{children:"Seen"})),l||(l=(0,g.jsx)("th",{children:"Role"})),(0,g.jsx)("th",{style:{width:"34px"}})]})}),(0,g.jsx)("tbody",{children:s.map(((e,s)=>(0,g.jsxs)("tr",{children:[(0,g.jsx)("td",{className:"width-2 text-center",children:(0,g.jsx)("img",{className:"filter-table__avatar",src:e.avatarUrl,alt:"User avatar"})}),(0,g.jsx)("td",{className:"max-width-6",children:(0,g.jsx)("span",{className:"ellipsis",title:e.login,children:e.login})}),(0,g.jsx)("td",{className:"max-width-5",children:(0,g.jsx)("span",{className:"ellipsis",title:e.email,children:e.email})}),(0,g.jsx)("td",{className:"max-width-5",children:(0,g.jsx)("span",{className:"ellipsis",title:e.name,children:e.name})}),(0,g.jsx)("td",{className:"width-1",children:e.lastSeenAtAge}),(0,g.jsx)("td",{className:"width-8",children:p.Vt.licensedAccessControlEnabled()?(0,g.jsx)(h.R,{userId:e.userId,orgId:t,builtInRole:e.role,onBuiltinRoleChange:s=>v(s,e),roleOptions:I,builtInRoles:y,disabled:!p.Vt.hasPermissionInMetadata(x.bW.OrgUsersRoleUpdate,e)}):(0,g.jsx)(m.A,{"aria-label":"Role",value:e.role,disabled:!p.Vt.hasPermissionInMetadata(x.bW.OrgUsersRoleUpdate,e),onChange:s=>v(s,e)})}),p.Vt.hasPermissionInMetadata(x.bW.OrgUsersRemove,e)&&(0,g.jsx)("td",{children:(0,g.jsx)(d.Button,{size:"sm",variant:"destructive",onClick:()=>{f(e)},icon:"times","aria-label":"Delete user"})})]},`${e.userId}-${s}`)))})]}),Boolean(b)&&(0,g.jsx)(d.ConfirmModal,{body:`Are you sure you want to delete user ${null==b?void 0:b.login}?`,confirmText:"Delete",title:"Delete",onDismiss:()=>{f(null)},isOpen:!0,onConfirm:()=>{b&&(j(b),f(null))}})]})}}}]);
//# sourceMappingURL=UsersListPage.0dfd49f78dc93c695e30.js.map