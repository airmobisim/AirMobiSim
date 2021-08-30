// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: airmobisim.proto

#include "airmobisim.pb.h"

#include <algorithm>

#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/wire_format_lite.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>

PROTOBUF_PRAGMA_INIT_SEG
namespace airmobisim {
constexpr Response::Response(
  ::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized)
  : id_(0)
  , x_(0)
  , y_(0)
  , z_(0){}
struct ResponseDefaultTypeInternal {
  constexpr ResponseDefaultTypeInternal()
    : _instance(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized{}) {}
  ~ResponseDefaultTypeInternal() {}
  union {
    Response _instance;
  };
};
PROTOBUF_ATTRIBUTE_NO_DESTROY PROTOBUF_CONSTINIT ResponseDefaultTypeInternal _Response_default_instance_;
constexpr ResponseQuery::ResponseQuery(
  ::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized)
  : responses_(){}
struct ResponseQueryDefaultTypeInternal {
  constexpr ResponseQueryDefaultTypeInternal()
    : _instance(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized{}) {}
  ~ResponseQueryDefaultTypeInternal() {}
  union {
    ResponseQuery _instance;
  };
};
PROTOBUF_ATTRIBUTE_NO_DESTROY PROTOBUF_CONSTINIT ResponseQueryDefaultTypeInternal _ResponseQuery_default_instance_;
}  // namespace airmobisim
static ::PROTOBUF_NAMESPACE_ID::Metadata file_level_metadata_airmobisim_2eproto[2];
static constexpr ::PROTOBUF_NAMESPACE_ID::EnumDescriptor const** file_level_enum_descriptors_airmobisim_2eproto = nullptr;
static constexpr ::PROTOBUF_NAMESPACE_ID::ServiceDescriptor const** file_level_service_descriptors_airmobisim_2eproto = nullptr;

const ::PROTOBUF_NAMESPACE_ID::uint32 TableStruct_airmobisim_2eproto::offsets[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) = {
  ~0u,  // no _has_bits_
  PROTOBUF_FIELD_OFFSET(::airmobisim::Response, _internal_metadata_),
  ~0u,  // no _extensions_
  ~0u,  // no _oneof_case_
  ~0u,  // no _weak_field_map_
  PROTOBUF_FIELD_OFFSET(::airmobisim::Response, id_),
  PROTOBUF_FIELD_OFFSET(::airmobisim::Response, x_),
  PROTOBUF_FIELD_OFFSET(::airmobisim::Response, y_),
  PROTOBUF_FIELD_OFFSET(::airmobisim::Response, z_),
  ~0u,  // no _has_bits_
  PROTOBUF_FIELD_OFFSET(::airmobisim::ResponseQuery, _internal_metadata_),
  ~0u,  // no _extensions_
  ~0u,  // no _oneof_case_
  ~0u,  // no _weak_field_map_
  PROTOBUF_FIELD_OFFSET(::airmobisim::ResponseQuery, responses_),
};
static const ::PROTOBUF_NAMESPACE_ID::internal::MigrationSchema schemas[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) = {
  { 0, -1, sizeof(::airmobisim::Response)},
  { 9, -1, sizeof(::airmobisim::ResponseQuery)},
};

static ::PROTOBUF_NAMESPACE_ID::Message const * const file_default_instances[] = {
  reinterpret_cast<const ::PROTOBUF_NAMESPACE_ID::Message*>(&::airmobisim::_Response_default_instance_),
  reinterpret_cast<const ::PROTOBUF_NAMESPACE_ID::Message*>(&::airmobisim::_ResponseQuery_default_instance_),
};

const char descriptor_table_protodef_airmobisim_2eproto[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) =
  "\n\020airmobisim.proto\022\nairmobisim\032\033google/p"
  "rotobuf/empty.proto\"7\n\010Response\022\n\n\002id\030\001 "
  "\001(\005\022\t\n\001x\030\002 \001(\002\022\t\n\001y\030\003 \001(\002\022\t\n\001z\030\004 \001(\002\"8\n\r"
  "ResponseQuery\022\'\n\tresponses\030\001 \003(\0132\024.airmo"
  "bisim.Response2\310\001\n\nAirMobiSim\0227\n\005Start\022\026"
  ".google.protobuf.Empty\032\026.google.protobuf"
  ".Empty\022G\n\022ExecuteOneTimeStep\022\026.google.pr"
  "otobuf.Empty\032\031.airmobisim.ResponseQuery\022"
  "8\n\006Finish\022\026.google.protobuf.Empty\032\026.goog"
  "le.protobuf.Emptyb\006proto3"
  ;
static const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable*const descriptor_table_airmobisim_2eproto_deps[1] = {
  &::descriptor_table_google_2fprotobuf_2fempty_2eproto,
};
static ::PROTOBUF_NAMESPACE_ID::internal::once_flag descriptor_table_airmobisim_2eproto_once;
const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_airmobisim_2eproto = {
  false, false, 385, descriptor_table_protodef_airmobisim_2eproto, "airmobisim.proto", 
  &descriptor_table_airmobisim_2eproto_once, descriptor_table_airmobisim_2eproto_deps, 1, 2,
  schemas, file_default_instances, TableStruct_airmobisim_2eproto::offsets,
  file_level_metadata_airmobisim_2eproto, file_level_enum_descriptors_airmobisim_2eproto, file_level_service_descriptors_airmobisim_2eproto,
};
PROTOBUF_ATTRIBUTE_WEAK ::PROTOBUF_NAMESPACE_ID::Metadata
descriptor_table_airmobisim_2eproto_metadata_getter(int index) {
  ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&descriptor_table_airmobisim_2eproto);
  return descriptor_table_airmobisim_2eproto.file_level_metadata[index];
}

// Force running AddDescriptors() at dynamic initialization time.
PROTOBUF_ATTRIBUTE_INIT_PRIORITY static ::PROTOBUF_NAMESPACE_ID::internal::AddDescriptorsRunner dynamic_init_dummy_airmobisim_2eproto(&descriptor_table_airmobisim_2eproto);
namespace airmobisim {

// ===================================================================

class Response::_Internal {
 public:
};

Response::Response(::PROTOBUF_NAMESPACE_ID::Arena* arena)
  : ::PROTOBUF_NAMESPACE_ID::Message(arena) {
  SharedCtor();
  RegisterArenaDtor(arena);
  // @@protoc_insertion_point(arena_constructor:airmobisim.Response)
}
Response::Response(const Response& from)
  : ::PROTOBUF_NAMESPACE_ID::Message() {
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  ::memcpy(&id_, &from.id_,
    static_cast<size_t>(reinterpret_cast<char*>(&z_) -
    reinterpret_cast<char*>(&id_)) + sizeof(z_));
  // @@protoc_insertion_point(copy_constructor:airmobisim.Response)
}

void Response::SharedCtor() {
::memset(reinterpret_cast<char*>(this) + static_cast<size_t>(
    reinterpret_cast<char*>(&id_) - reinterpret_cast<char*>(this)),
    0, static_cast<size_t>(reinterpret_cast<char*>(&z_) -
    reinterpret_cast<char*>(&id_)) + sizeof(z_));
}

Response::~Response() {
  // @@protoc_insertion_point(destructor:airmobisim.Response)
  SharedDtor();
  _internal_metadata_.Delete<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

void Response::SharedDtor() {
  GOOGLE_DCHECK(GetArena() == nullptr);
}

void Response::ArenaDtor(void* object) {
  Response* _this = reinterpret_cast< Response* >(object);
  (void)_this;
}
void Response::RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena*) {
}
void Response::SetCachedSize(int size) const {
  _cached_size_.Set(size);
}

void Response::Clear() {
// @@protoc_insertion_point(message_clear_start:airmobisim.Response)
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  ::memset(&id_, 0, static_cast<size_t>(
      reinterpret_cast<char*>(&z_) -
      reinterpret_cast<char*>(&id_)) + sizeof(z_));
  _internal_metadata_.Clear<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

const char* Response::_InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) {
#define CHK_(x) if (PROTOBUF_PREDICT_FALSE(!(x))) goto failure
  while (!ctx->Done(&ptr)) {
    ::PROTOBUF_NAMESPACE_ID::uint32 tag;
    ptr = ::PROTOBUF_NAMESPACE_ID::internal::ReadTag(ptr, &tag);
    CHK_(ptr);
    switch (tag >> 3) {
      // int32 id = 1;
      case 1:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 8)) {
          id_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint64(&ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      // float x = 2;
      case 2:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 21)) {
          x_ = ::PROTOBUF_NAMESPACE_ID::internal::UnalignedLoad<float>(ptr);
          ptr += sizeof(float);
        } else goto handle_unusual;
        continue;
      // float y = 3;
      case 3:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 29)) {
          y_ = ::PROTOBUF_NAMESPACE_ID::internal::UnalignedLoad<float>(ptr);
          ptr += sizeof(float);
        } else goto handle_unusual;
        continue;
      // float z = 4;
      case 4:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 37)) {
          z_ = ::PROTOBUF_NAMESPACE_ID::internal::UnalignedLoad<float>(ptr);
          ptr += sizeof(float);
        } else goto handle_unusual;
        continue;
      default: {
      handle_unusual:
        if ((tag & 7) == 4 || tag == 0) {
          ctx->SetLastTag(tag);
          goto success;
        }
        ptr = UnknownFieldParse(tag,
            _internal_metadata_.mutable_unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(),
            ptr, ctx);
        CHK_(ptr != nullptr);
        continue;
      }
    }  // switch
  }  // while
success:
  return ptr;
failure:
  ptr = nullptr;
  goto success;
#undef CHK_
}

::PROTOBUF_NAMESPACE_ID::uint8* Response::_InternalSerialize(
    ::PROTOBUF_NAMESPACE_ID::uint8* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const {
  // @@protoc_insertion_point(serialize_to_array_start:airmobisim.Response)
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  // int32 id = 1;
  if (this->id() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteInt32ToArray(1, this->_internal_id(), target);
  }

  // float x = 2;
  if (!(this->x() <= 0 && this->x() >= 0)) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteFloatToArray(2, this->_internal_x(), target);
  }

  // float y = 3;
  if (!(this->y() <= 0 && this->y() >= 0)) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteFloatToArray(3, this->_internal_y(), target);
  }

  // float z = 4;
  if (!(this->z() <= 0 && this->z() >= 0)) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteFloatToArray(4, this->_internal_z(), target);
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormat::InternalSerializeUnknownFieldsToArray(
        _internal_metadata_.unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(::PROTOBUF_NAMESPACE_ID::UnknownFieldSet::default_instance), target, stream);
  }
  // @@protoc_insertion_point(serialize_to_array_end:airmobisim.Response)
  return target;
}

size_t Response::ByteSizeLong() const {
// @@protoc_insertion_point(message_byte_size_start:airmobisim.Response)
  size_t total_size = 0;

  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  // int32 id = 1;
  if (this->id() != 0) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::Int32Size(
        this->_internal_id());
  }

  // float x = 2;
  if (!(this->x() <= 0 && this->x() >= 0)) {
    total_size += 1 + 4;
  }

  // float y = 3;
  if (!(this->y() <= 0 && this->y() >= 0)) {
    total_size += 1 + 4;
  }

  // float z = 4;
  if (!(this->z() <= 0 && this->z() >= 0)) {
    total_size += 1 + 4;
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    return ::PROTOBUF_NAMESPACE_ID::internal::ComputeUnknownFieldsSize(
        _internal_metadata_, total_size, &_cached_size_);
  }
  int cached_size = ::PROTOBUF_NAMESPACE_ID::internal::ToCachedSize(total_size);
  SetCachedSize(cached_size);
  return total_size;
}

void Response::MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) {
// @@protoc_insertion_point(generalized_merge_from_start:airmobisim.Response)
  GOOGLE_DCHECK_NE(&from, this);
  const Response* source =
      ::PROTOBUF_NAMESPACE_ID::DynamicCastToGenerated<Response>(
          &from);
  if (source == nullptr) {
  // @@protoc_insertion_point(generalized_merge_from_cast_fail:airmobisim.Response)
    ::PROTOBUF_NAMESPACE_ID::internal::ReflectionOps::Merge(from, this);
  } else {
  // @@protoc_insertion_point(generalized_merge_from_cast_success:airmobisim.Response)
    MergeFrom(*source);
  }
}

void Response::MergeFrom(const Response& from) {
// @@protoc_insertion_point(class_specific_merge_from_start:airmobisim.Response)
  GOOGLE_DCHECK_NE(&from, this);
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  if (from.id() != 0) {
    _internal_set_id(from._internal_id());
  }
  if (!(from.x() <= 0 && from.x() >= 0)) {
    _internal_set_x(from._internal_x());
  }
  if (!(from.y() <= 0 && from.y() >= 0)) {
    _internal_set_y(from._internal_y());
  }
  if (!(from.z() <= 0 && from.z() >= 0)) {
    _internal_set_z(from._internal_z());
  }
}

void Response::CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) {
// @@protoc_insertion_point(generalized_copy_from_start:airmobisim.Response)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

void Response::CopyFrom(const Response& from) {
// @@protoc_insertion_point(class_specific_copy_from_start:airmobisim.Response)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

bool Response::IsInitialized() const {
  return true;
}

void Response::InternalSwap(Response* other) {
  using std::swap;
  _internal_metadata_.Swap<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(&other->_internal_metadata_);
  ::PROTOBUF_NAMESPACE_ID::internal::memswap<
      PROTOBUF_FIELD_OFFSET(Response, z_)
      + sizeof(Response::z_)
      - PROTOBUF_FIELD_OFFSET(Response, id_)>(
          reinterpret_cast<char*>(&id_),
          reinterpret_cast<char*>(&other->id_));
}

::PROTOBUF_NAMESPACE_ID::Metadata Response::GetMetadata() const {
  return GetMetadataStatic();
}


// ===================================================================

class ResponseQuery::_Internal {
 public:
};

ResponseQuery::ResponseQuery(::PROTOBUF_NAMESPACE_ID::Arena* arena)
  : ::PROTOBUF_NAMESPACE_ID::Message(arena),
  responses_(arena) {
  SharedCtor();
  RegisterArenaDtor(arena);
  // @@protoc_insertion_point(arena_constructor:airmobisim.ResponseQuery)
}
ResponseQuery::ResponseQuery(const ResponseQuery& from)
  : ::PROTOBUF_NAMESPACE_ID::Message(),
      responses_(from.responses_) {
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  // @@protoc_insertion_point(copy_constructor:airmobisim.ResponseQuery)
}

void ResponseQuery::SharedCtor() {
}

ResponseQuery::~ResponseQuery() {
  // @@protoc_insertion_point(destructor:airmobisim.ResponseQuery)
  SharedDtor();
  _internal_metadata_.Delete<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

void ResponseQuery::SharedDtor() {
  GOOGLE_DCHECK(GetArena() == nullptr);
}

void ResponseQuery::ArenaDtor(void* object) {
  ResponseQuery* _this = reinterpret_cast< ResponseQuery* >(object);
  (void)_this;
}
void ResponseQuery::RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena*) {
}
void ResponseQuery::SetCachedSize(int size) const {
  _cached_size_.Set(size);
}

void ResponseQuery::Clear() {
// @@protoc_insertion_point(message_clear_start:airmobisim.ResponseQuery)
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  responses_.Clear();
  _internal_metadata_.Clear<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

const char* ResponseQuery::_InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) {
#define CHK_(x) if (PROTOBUF_PREDICT_FALSE(!(x))) goto failure
  while (!ctx->Done(&ptr)) {
    ::PROTOBUF_NAMESPACE_ID::uint32 tag;
    ptr = ::PROTOBUF_NAMESPACE_ID::internal::ReadTag(ptr, &tag);
    CHK_(ptr);
    switch (tag >> 3) {
      // repeated .airmobisim.Response responses = 1;
      case 1:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 10)) {
          ptr -= 1;
          do {
            ptr += 1;
            ptr = ctx->ParseMessage(_internal_add_responses(), ptr);
            CHK_(ptr);
            if (!ctx->DataAvailable(ptr)) break;
          } while (::PROTOBUF_NAMESPACE_ID::internal::ExpectTag<10>(ptr));
        } else goto handle_unusual;
        continue;
      default: {
      handle_unusual:
        if ((tag & 7) == 4 || tag == 0) {
          ctx->SetLastTag(tag);
          goto success;
        }
        ptr = UnknownFieldParse(tag,
            _internal_metadata_.mutable_unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(),
            ptr, ctx);
        CHK_(ptr != nullptr);
        continue;
      }
    }  // switch
  }  // while
success:
  return ptr;
failure:
  ptr = nullptr;
  goto success;
#undef CHK_
}

::PROTOBUF_NAMESPACE_ID::uint8* ResponseQuery::_InternalSerialize(
    ::PROTOBUF_NAMESPACE_ID::uint8* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const {
  // @@protoc_insertion_point(serialize_to_array_start:airmobisim.ResponseQuery)
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  // repeated .airmobisim.Response responses = 1;
  for (unsigned int i = 0,
      n = static_cast<unsigned int>(this->_internal_responses_size()); i < n; i++) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::
      InternalWriteMessage(1, this->_internal_responses(i), target, stream);
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormat::InternalSerializeUnknownFieldsToArray(
        _internal_metadata_.unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(::PROTOBUF_NAMESPACE_ID::UnknownFieldSet::default_instance), target, stream);
  }
  // @@protoc_insertion_point(serialize_to_array_end:airmobisim.ResponseQuery)
  return target;
}

size_t ResponseQuery::ByteSizeLong() const {
// @@protoc_insertion_point(message_byte_size_start:airmobisim.ResponseQuery)
  size_t total_size = 0;

  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  // repeated .airmobisim.Response responses = 1;
  total_size += 1UL * this->_internal_responses_size();
  for (const auto& msg : this->responses_) {
    total_size +=
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::MessageSize(msg);
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    return ::PROTOBUF_NAMESPACE_ID::internal::ComputeUnknownFieldsSize(
        _internal_metadata_, total_size, &_cached_size_);
  }
  int cached_size = ::PROTOBUF_NAMESPACE_ID::internal::ToCachedSize(total_size);
  SetCachedSize(cached_size);
  return total_size;
}

void ResponseQuery::MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) {
// @@protoc_insertion_point(generalized_merge_from_start:airmobisim.ResponseQuery)
  GOOGLE_DCHECK_NE(&from, this);
  const ResponseQuery* source =
      ::PROTOBUF_NAMESPACE_ID::DynamicCastToGenerated<ResponseQuery>(
          &from);
  if (source == nullptr) {
  // @@protoc_insertion_point(generalized_merge_from_cast_fail:airmobisim.ResponseQuery)
    ::PROTOBUF_NAMESPACE_ID::internal::ReflectionOps::Merge(from, this);
  } else {
  // @@protoc_insertion_point(generalized_merge_from_cast_success:airmobisim.ResponseQuery)
    MergeFrom(*source);
  }
}

void ResponseQuery::MergeFrom(const ResponseQuery& from) {
// @@protoc_insertion_point(class_specific_merge_from_start:airmobisim.ResponseQuery)
  GOOGLE_DCHECK_NE(&from, this);
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  responses_.MergeFrom(from.responses_);
}

void ResponseQuery::CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) {
// @@protoc_insertion_point(generalized_copy_from_start:airmobisim.ResponseQuery)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

void ResponseQuery::CopyFrom(const ResponseQuery& from) {
// @@protoc_insertion_point(class_specific_copy_from_start:airmobisim.ResponseQuery)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

bool ResponseQuery::IsInitialized() const {
  return true;
}

void ResponseQuery::InternalSwap(ResponseQuery* other) {
  using std::swap;
  _internal_metadata_.Swap<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(&other->_internal_metadata_);
  responses_.InternalSwap(&other->responses_);
}

::PROTOBUF_NAMESPACE_ID::Metadata ResponseQuery::GetMetadata() const {
  return GetMetadataStatic();
}


// @@protoc_insertion_point(namespace_scope)
}  // namespace airmobisim
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_NOINLINE ::airmobisim::Response* Arena::CreateMaybeMessage< ::airmobisim::Response >(Arena* arena) {
  return Arena::CreateMessageInternal< ::airmobisim::Response >(arena);
}
template<> PROTOBUF_NOINLINE ::airmobisim::ResponseQuery* Arena::CreateMaybeMessage< ::airmobisim::ResponseQuery >(Arena* arena) {
  return Arena::CreateMessageInternal< ::airmobisim::ResponseQuery >(arena);
}
PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)
#include <google/protobuf/port_undef.inc>
