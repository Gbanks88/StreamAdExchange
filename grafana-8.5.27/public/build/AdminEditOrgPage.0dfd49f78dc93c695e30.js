"use strict";(self.webpackChunkgrafana=self.webpackChunkgrafana||[]).push([[2721],{"./public/app/features/admin/AdminEditOrgPage.tsx":(e,s,a)=>{a.r(s),a.d(s,{default:()=>f});var r,t,n,i=a("./.yarn/__virtual__/@emotion-css-virtual-72c314ddb1/3/opt/drone/yarncache/@emotion-css-npm-11.7.1-25ff8755a7-ac1f56656f.zip/node_modules/@emotion/css/dist/emotion-css.esm.js"),c=a("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),l=a("./.yarn/__virtual__/react-redux-virtual-7ad20a440e/3/opt/drone/yarncache/react-redux-npm-7.2.6-134f5ed64d-0bf142ce0d.zip/node_modules/react-redux/es/index.js"),o=a("./.yarn/__virtual__/react-use-virtual-00326e70ba/3/opt/drone/yarncache/react-use-npm-17.3.2-a032cbeb01-7379460f51.zip/node_modules/react-use/esm/useAsyncFn.js"),d=a("./packages/grafana-runtime/src/index.ts"),u=a("./packages/grafana-ui/src/index.ts"),p=a("./public/app/core/components/Page/Page.tsx"),m=a("./public/app/core/core.ts"),h=a("./public/app/core/selectors/navModel.ts"),g=a("./public/app/core/utils/accessControl.ts"),x=a("./public/app/types/index.ts"),b=a("./public/app/features/users/UsersTable.tsx"),j=a("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/jsx-runtime.js");function f(e){let{match:s}=e;const a=(0,l.useSelector)((e=>e.navIndex)),f=(0,h.h)(a,"global-orgs"),v=parseInt(s.params.id,10),y=m.Vt.hasPermission(x.bW.OrgsWrite),R=m.Vt.hasPermission(x.bW.OrgUsersRead),[_,I]=(0,c.useState)([]),[N,w]=(0,o.Z)((()=>(async e=>await(0,d.getBackendSrv)().get("/api/orgs/"+e))(v)),[]),[,k]=(0,o.Z)((()=>(async e=>m.Vt.hasPermission(x.bW.OrgUsersRead)?await(0,d.getBackendSrv)().get(`/api/orgs/${e}/users`,(0,g.y)()):[])(v)),[]);(0,c.useEffect)((()=>{w(),k().then((e=>I(e)))}),[w,k]);return(0,j.jsx)(p.Z,{navModel:f,children:(0,j.jsx)(p.Z.Contents,{children:(0,j.jsxs)(j.Fragment,{children:[t||(t=(0,j.jsx)(u.Legend,{children:"Edit organization"})),N.value&&(0,j.jsx)(u.Form,{defaultValues:{orgName:N.value.name},onSubmit:async e=>await(async e=>await(0,d.getBackendSrv)().put("/api/orgs/"+v,Object.assign({},N.value,{name:e})))(e.orgName),children:e=>{let{register:s,errors:a}=e;return(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(u.Field,{label:"Name",invalid:!!a.orgName,error:"Name is required",disabled:!y,children:(0,j.jsx)(u.Input,Object.assign({},s("orgName",{required:!0}),{id:"org-name-input"}))}),(0,j.jsx)(u.Button,{disabled:!y,children:"Update"})]})}}),(0,j.jsxs)("div",{className:i.css`
              margin-top: 20px;
            `,children:[n||(n=(0,j.jsx)(u.Legend,{children:"Organization users"})),!R&&(r||(r=(0,j.jsx)(u.Alert,{severity:"info",title:"Access denied",children:"You do not have permission to see users in this organization. To update this organization, contact your server administrator."}))),R&&!!_.length&&(0,j.jsx)(b.Z,{users:_,orgId:v,onRoleChange:(e,s)=>{(async(e,s)=>{await(0,d.getBackendSrv)().patch("/api/orgs/"+s+"/users/"+e.userId,e)})(Object.assign({},s,{role:e}),v),I(_.map((a=>s.userId===a.userId?Object.assign({},s,{role:e}):a))),k()},onRemoveUser:e=>{(async(e,s)=>{await(0,d.getBackendSrv)().delete("/api/orgs/"+s+"/users/"+e.userId)})(e,v),I(_.filter((s=>e.userId!==s.userId))),k()}})]})]})})})}},"./public/app/features/users/UsersTable.tsx":(e,s,a)=>{a.d(s,{Z:()=>b});var r,t,n,i,c,l,o=a("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),d=a("./packages/grafana-ui/src/index.ts"),u=a("./public/app/core/components/RolePicker/UserRolePicker.tsx"),p=a("./public/app/core/components/RolePicker/api.ts"),m=a("./public/app/core/core.ts"),h=a("./public/app/types/index.ts"),g=a("./public/app/features/admin/OrgRolePicker.tsx"),x=a("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/jsx-runtime.js");const b=e=>{const{users:s,orgId:a,onRoleChange:b,onRemoveUser:j}=e,[f,v]=(0,o.useState)(null),[y,R]=(0,o.useState)([]),[_,I]=(0,o.useState)({});return(0,o.useEffect)((()=>{m.Vt.licensedAccessControlEnabled()&&async function(){try{if(m.Vt.hasPermission(h.bW.ActionRolesList)){let e=await(0,p.ul)(a);R(e)}if(m.Vt.hasPermission(h.bW.ActionBuiltinRolesList)){const e=await(0,p.fh)(a);I(e)}}catch(e){console.error("Error loading options")}}()}),[a]),(0,x.jsxs)(x.Fragment,{children:[(0,x.jsxs)("table",{className:"filter-table form-inline",children:[(0,x.jsx)("thead",{children:(0,x.jsxs)("tr",{children:[r||(r=(0,x.jsx)("th",{})),t||(t=(0,x.jsx)("th",{children:"Login"})),n||(n=(0,x.jsx)("th",{children:"Email"})),i||(i=(0,x.jsx)("th",{children:"Name"})),c||(c=(0,x.jsx)("th",{children:"Seen"})),l||(l=(0,x.jsx)("th",{children:"Role"})),(0,x.jsx)("th",{style:{width:"34px"}})]})}),(0,x.jsx)("tbody",{children:s.map(((e,s)=>(0,x.jsxs)("tr",{children:[(0,x.jsx)("td",{className:"width-2 text-center",children:(0,x.jsx)("img",{className:"filter-table__avatar",src:e.avatarUrl,alt:"User avatar"})}),(0,x.jsx)("td",{className:"max-width-6",children:(0,x.jsx)("span",{className:"ellipsis",title:e.login,children:e.login})}),(0,x.jsx)("td",{className:"max-width-5",children:(0,x.jsx)("span",{className:"ellipsis",title:e.email,children:e.email})}),(0,x.jsx)("td",{className:"max-width-5",children:(0,x.jsx)("span",{className:"ellipsis",title:e.name,children:e.name})}),(0,x.jsx)("td",{className:"width-1",children:e.lastSeenAtAge}),(0,x.jsx)("td",{className:"width-8",children:m.Vt.licensedAccessControlEnabled()?(0,x.jsx)(u.R,{userId:e.userId,orgId:a,builtInRole:e.role,onBuiltinRoleChange:s=>b(s,e),roleOptions:y,builtInRoles:_,disabled:!m.Vt.hasPermissionInMetadata(h.bW.OrgUsersRoleUpdate,e)}):(0,x.jsx)(g.A,{"aria-label":"Role",value:e.role,disabled:!m.Vt.hasPermissionInMetadata(h.bW.OrgUsersRoleUpdate,e),onChange:s=>b(s,e)})}),m.Vt.hasPermissionInMetadata(h.bW.OrgUsersRemove,e)&&(0,x.jsx)("td",{children:(0,x.jsx)(d.Button,{size:"sm",variant:"destructive",onClick:()=>{v(e)},icon:"times","aria-label":"Delete user"})})]},`${e.userId}-${s}`)))})]}),Boolean(f)&&(0,x.jsx)(d.ConfirmModal,{body:`Are you sure you want to delete user ${null==f?void 0:f.login}?`,confirmText:"Delete",title:"Delete",onDismiss:()=>{v(null)},isOpen:!0,onConfirm:()=>{f&&(j(f),v(null))}})]})}}}]);
//# sourceMappingURL=AdminEditOrgPage.0dfd49f78dc93c695e30.js.map